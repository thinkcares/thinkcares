using System;
using System.IO;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Google.Cloud.BigQuery.V2;
using Google.Cloud.Storage.V1;
using Google.Apis.Auth.OAuth2;
using System.Configuration;
using System.Diagnostics;

namespace BigQuery
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            DateTime horaInicio = DateTime.Now;
            txtHoraInicio.Text = horaInicio.ToString();
            string sProjectID = ConfigurationManager.AppSettings["ProjectID"];
            string sDatasetId = ConfigurationManager.AppSettings["DatasetId"];
            string sAuthJasonPathFile = ConfigurationManager.AppSettings["AuthJasonPathFile"];
            string sBucketPathToLoadCsvSET = ConfigurationManager.AppSettings["BucketPathToLoadCsvSET"];
            

            List<string> lstCmdsSqlExtract = new List<string>();
            foreach (string key in ConfigurationManager.AppSettings)
            {
                if (key.StartsWith("ExtractMSSQL2csv"))
                {
                    string value = ConfigurationManager.AppSettings[key];
                    lstCmdsSqlExtract.Add(value);
                }

            }

            
            List<string> lstCmdsCopyGS = new List<string>();
            foreach (string key in ConfigurationManager.AppSettings)
            {
                if (key.StartsWith("CopyGS"))
                {
                    string value = ConfigurationManager.AppSettings[key];
                    lstCmdsCopyGS.Add(value);
                }

            }
            //bqCmd1
            List<string> lstCmdsbqCmd = new List<string>();
            foreach (string key in ConfigurationManager.AppSettings)
            {
                if (key.StartsWith("bqCmd"))
                {
                    string value = ConfigurationManager.AppSettings[key];
                    lstCmdsbqCmd.Add(value);
                }

            }


            var credential = GoogleCredential.FromFile(sAuthJasonPathFile);
            //var storage = StorageClient.Create(credential);
            //var bq = StorageClient.Create(credential);
            // Make an authenticated API request. //var buckets = storage.ListBuckets(projectId);
            //List<String> BucketList = new List<string>();
            //foreach (var bucket in buckets)
            //{
            //    BucketList.Add(bucket.Name);
            //}
            BigQueryClean(sProjectID, sDatasetId,credential);

            //MessageBox.Show("Proceso BigQuery Clean Finalizado");
            //foreach (var sql in lstCmdsSqlExtract)
            //{
            //    EjecutarCmd("cd /tmp && " + sql.Replace("'", "\""));
            //}
            

            LimpiaSed(@"C:\tmp");



            foreach (var file in lstCmdsCopyGS)
            {
                EjecutarCmd("cd /tmp && " + file.Replace("'", "\""));
            }
            // MessageBox.Show("Proceso GS Copy Command Finalizado");

            foreach (var bqcmd in lstCmdsbqCmd)
            {
                Console.WriteLine(bqcmd.Replace("'", "\""));
                EjecutarCmd(bqcmd.Replace("'", "\""));
            }
            // MessageBox.Show("Proceso bq  Command Finalizado");


            DateTime horaFin = DateTime.Now;
            txtHoraFin.Text = horaFin.ToString();
            MessageBox.Show("Proceso Finalizado Totalmente");
            


        }

        public static void EjecutarCmd(string comando)
            {
            try
            {
                Process cmd = new Process();
                cmd.StartInfo.FileName = "cmd.exe";
                cmd.StartInfo.WorkingDirectory = @"C:\tmp";
                cmd.StartInfo.RedirectStandardInput = true;
                cmd.StartInfo.RedirectStandardOutput = true;
                cmd.StartInfo.CreateNoWindow = true;
                cmd.StartInfo.UseShellExecute = false;
                cmd.Start();
                cmd.StandardInput.WriteLine(comando);
                cmd.StandardInput.Flush();
                cmd.StandardInput.Close();
                cmd.WaitForExit();
                // MessageBox.Show(cmd.StandardOutput.ReadToEnd());
            }
            catch (Exception ex)
            {

                MessageBox.Show(ex.Message.ToString());
            }
            
            
           
        }
        public static void BigQueryClean(string sProjectID, string sDatasetId, GoogleCredential credential)
        {
            var bqClient = BigQueryClient.Create(sProjectID, credential);
            try
            {
                List<string> lstTblsFinal = new List<string>();
                foreach (var table in bqClient.ListTables(sDatasetId).ToList<BigQueryTable>())
                {
                    string n = table.Resource.Type;
                    if (n == "TABLE")
                    {
                        lstTblsFinal.Add(table.Reference.TableId);
                    }
                }
                MessageBox.Show("Tablas encontradas en :" + lstTblsFinal.Count.ToString());
                if (lstTblsFinal.Count() > 0)
                {
                    foreach (var tbl in lstTblsFinal)
                    {
                        bqClient.DeleteTable(sDatasetId, tbl);
                    }
                }



            }
            catch (Exception ex)
            {

                MessageBox.Show(ex.Message);
            }
        }

        public static void LimpiaSed(string path)
        {
            try
            {
                string[] files = System.IO.Directory.GetFiles(path, "*.csv");

               
                foreach (var file in files)
                {
                    string patron = @"sed -i'.bck' 's/\NULL//g' ";
                    patron = patron.Replace("'","\"") + file;
                    EjecutarCmd(patron);
                    Console.WriteLine(patron);
                    if (File.Exists(file+".bck"))
                    {
                        File.Delete(file+".bck");
                        File.Delete("sed*.*");
                    }
                    Comprime(file);
                }
            }
            catch (Exception ex)
            {

                MessageBox.Show(ex.Message);
            }
            
        }
        public static void Comprime(string file){
            FileInfo fi = new FileInfo(file);
            string comando7zip = String.Format("7z a -tgzip {0}.gz {0} -MX3",fi.Name);
            Console.WriteLine(comando7zip);
            EjecutarCmd(comando7zip);

            if (File.Exists(fi.FullName))
            {
                File.Delete(fi.FullName);
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }
    }
}
