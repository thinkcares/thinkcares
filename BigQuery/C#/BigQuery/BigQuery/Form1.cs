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
        public static List<string> lstCmdsSqlExtract = new List<string>();
        public static List<string> lstCmdsbqCmd = new List<string>();
        public static List<string> lstCmdsCopyGS = new List<string>();
        public static string sAuthJasonPathFile = ConfigurationManager.AppSettings["AuthJasonPathFile"];
        public static GoogleCredential credential = GoogleCredential.FromFile(sAuthJasonPathFile);
        public static string sProjectID;
        public static string sDatasetId;
        public static string sBucketPathToLoadCsvSET;
        public static TextWriterTraceListener twl = new TextWriterTraceListener(@"C:\tmp\log.txt");


        public Form1()
        {
            InitializeComponent();

        }

        private void button1_Click(object sender, EventArgs e)
        {
            DateTime horaInicio = DateTime.Now;
            txtHoraInicio.Text = horaInicio.ToString();
            InicializaVariables();
            Debug.Listeners.Add(twl);
            Trace.WriteLine(">>>> Inicia gCloud ");
            BuscaArchivosGS(sProjectID, credential); // Busca Files en el bucket destino y borra todos los files en éste
            BigQueryClean(sProjectID, sDatasetId,credential); // Borra tablas en BigQuery
            ExtractSql2Csv(); // Extrae datos de MSSQL a archivos Csv
            LimpiaSed(@"C:\tmp"); // Limpia, comprime csvs en 7zip
            Upload2GS(); // sube archivos a Google Storage
            LoadBq(); // Inserta archivos en tablas de BigQuery
            BigQueryUpdate(sProjectID, sDatasetId, credential);
            DateTime horaFin = DateTime.Now;
            txtHoraFin.Text = horaFin.ToString();
            MessageBox.Show("Proceso Finalizado Totalmente");


        }
        public static void LoadBq()
        {
            foreach (var bqcmd in lstCmdsbqCmd)
            {
                //Console.WriteLine(bqcmd.Replace("'", "\""));
                EjecutarCmd(bqcmd.Replace("'", "\""));
            }
        }
        public static void Upload2GS()
        {  foreach (var file in lstCmdsCopyGS)
            {
                EjecutarCmd(file.Replace("'", "\""));
            }
         }
        public static void ExtractSql2Csv()
        {
            foreach (var sql in lstCmdsSqlExtract)
            {
                
               EjecutarCmd(sql.Replace("'", "\""));
            }

        }
        public static bool InicializaVariables()
        {
            bool bandera = false;
            try
            {
             sProjectID = ConfigurationManager.AppSettings["ProjectID"];
             sDatasetId = ConfigurationManager.AppSettings["DatasetId"];
             
             sBucketPathToLoadCsvSET = ConfigurationManager.AppSettings["BucketPathToLoadCsvSET"];
            foreach (string key in ConfigurationManager.AppSettings)
            {
                if (key.StartsWith("ExtractMSSQL2csv"))
                {
                    string value = ConfigurationManager.AppSettings[key];
                    lstCmdsSqlExtract.Add(value);
                }
            }
            foreach (string key in ConfigurationManager.AppSettings)
            {
                if (key.StartsWith("CopyGS"))
                {
                    string value = ConfigurationManager.AppSettings[key];
                    lstCmdsCopyGS.Add(value);
                }
            }
            foreach (string key in ConfigurationManager.AppSettings)
            {
                if (key.StartsWith("bqCmd"))
                {
                    string value = ConfigurationManager.AppSettings[key];
                    lstCmdsbqCmd.Add(value);
                }
            }
                bandera = true;
            }
            catch (Exception ex)
            {

                MessageBox.Show(ex.Message);
            }
            return bandera;
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
                Trace.WriteLine(comando);
                twl.Flush();

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
                        Trace.WriteLine(string.Format("Se borró la siguiente tabla en Bq: {0}", tbl));

                    }
                }
                else {
                    Trace.WriteLine("No se encontraron tablas en el Dataset");
                }

                twl.Flush();

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
                    string patron = @" cd /tmp && sed -i'.bck' 's/\NULL//g' ";
                    patron = patron.Replace("'","\"") + file.Replace(@"C:\tmp\","");
                    EjecutarCmd(patron);
                    Console.WriteLine(patron);
                    if (File.Exists(file+".bck"))
                    {
                        File.Delete(file+".bck");
                        
                    }
                    Comprime(file);

                    var dir = new DirectoryInfo(@"C:\tmp");
                    foreach (var item in dir.EnumerateFiles("sed*.*"))
                    {
                        item.Delete();
                    }
                   

                }
            }
            catch (Exception ex)
            {

                MessageBox.Show(ex.Message);
            }
            
        }
        public static void Comprime(string file){
            FileInfo fi = new FileInfo(file);
            string comando7zip = String.Format("cd /tmp && 7z a -tgzip {0}.gz {0} -MX3",fi.Name);
            Console.WriteLine(comando7zip);
            EjecutarCmd(comando7zip);

            if (File.Exists(fi.FullName))
            {
                File.Delete(fi.FullName);
            }
        }
        public static void BuscaArchivosGS(string sProjectID, GoogleCredential credential)
        {
            var storage = StorageClient.Create(credential);
           // Make an authenticated API request. 
            var buckets = storage.ListBuckets(sProjectID);
            List<string> lstFiles = new List<string>();
            foreach (var bucket in storage.ListObjects(@"hrdz_input", "").Where( o => o.Name.Contains("CsvFilesSet/")))
            {
               /// Console.WriteLine( bucket.Name);               
                lstFiles.Add(bucket.Name);
                
            }
            lstFiles.Remove("CsvFilesSet/");

            if (lstFiles.Count > 0)
            {
                DeleteObjectGStorage("hrdz_input", lstFiles, credential);
                foreach (var item in lstFiles)
                {
                    Trace.WriteLine(string.Format("Se eliminó el archivo en GS:->{0}", item));
                }
              
            }
            else
            {
                Trace.WriteLine("No se encontraron Archivos en el Google Storage");
            }

            twl.Flush();

        }
        public static  void DeleteObjectGStorage(string bucketName, IEnumerable<string> objectNames, GoogleCredential credential)
        {
            var storage = StorageClient.Create(credential);

            foreach (string objectName in objectNames)
            {
                storage.DeleteObject(bucketName, objectName);
                Console.WriteLine($"Deleted {objectName}.");
            }
        }
        public static void BigQueryUpdate(string sProjectID, string sDatasetId, GoogleCredential credential)
        {
            var bqClient = BigQueryClient.Create(sProjectID, credential);
            try
            {
                List<BigQueryParameter> parameters = new List<BigQueryParameter>();

                bqClient.ExecuteQuery("update sethdzqa.zimp_fact a  set a.no_doc_sap= trim(a.no_doc_sap) where 1=1"
                    ,parameters
                    , new QueryOptions { UseLegacySql = false });
                bqClient.ExecuteQuery("update sethdzqa.zexp_fact a  set a.no_doc_sap= trim(a.no_doc_sap) where 1=1"
                   , parameters
                   , new QueryOptions { UseLegacySql = false });
                bqClient.ExecuteQuery("update sethdzqa.det_arch_transfer a  set a.nom_arch= trim(a.nom_arch) where 1=1"
                   , parameters
                   , new QueryOptions { UseLegacySql = false });
                bqClient.ExecuteQuery("update sethdzqa.hist_movimiento a  set a.no_docto= trim(a.no_docto) where 1=1"
                   , parameters
                   , new QueryOptions { UseLegacySql = false });
                bqClient.ExecuteQuery("update sethdzqa.hist_solicitud a  set a.no_docto= trim(a.no_docto) where 1=1"
                , parameters
                , new QueryOptions { UseLegacySql = false });
                bqClient.ExecuteQuery("update sethdzqa.movimiento a  set a.no_docto= trim(a.no_docto) where 1=1"
                , parameters
                , new QueryOptions { UseLegacySql = false });


            }
            catch (Exception ex)
            {

                MessageBox.Show(ex.Message);
            }
        }
        private void Form1_Load(object sender, EventArgs e)
        {

        }

        
    }
}
