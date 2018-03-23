namespace BigQuery
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.button1 = new System.Windows.Forms.Button();
            this.txtHoraInicio = new System.Windows.Forms.TextBox();
            this.txtHoraFin = new System.Windows.Forms.TextBox();
            this.listCmdView = new System.Windows.Forms.ListView();
            this.columnHeader1 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.SuspendLayout();
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(584, 67);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(82, 31);
            this.button1.TabIndex = 0;
            this.button1.Text = "&Ejecutar";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // txtHoraInicio
            // 
            this.txtHoraInicio.Location = new System.Drawing.Point(38, 78);
            this.txtHoraInicio.Name = "txtHoraInicio";
            this.txtHoraInicio.Size = new System.Drawing.Size(207, 20);
            this.txtHoraInicio.TabIndex = 1;
            // 
            // txtHoraFin
            // 
            this.txtHoraFin.Location = new System.Drawing.Point(275, 78);
            this.txtHoraFin.Name = "txtHoraFin";
            this.txtHoraFin.Size = new System.Drawing.Size(207, 20);
            this.txtHoraFin.TabIndex = 2;
            // 
            // listCmdView
            // 
            this.listCmdView.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.columnHeader1});
            this.listCmdView.Location = new System.Drawing.Point(1, 140);
            this.listCmdView.Name = "listCmdView";
            this.listCmdView.Size = new System.Drawing.Size(787, 171);
            this.listCmdView.TabIndex = 3;
            this.listCmdView.UseCompatibleStateImageBehavior = false;
            this.listCmdView.View = System.Windows.Forms.View.Details;
            // 
            // columnHeader1
            // 
            this.columnHeader1.Text = "Comando";
            this.columnHeader1.Width = 785;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.listCmdView);
            this.Controls.Add(this.txtHoraFin);
            this.Controls.Add(this.txtHoraInicio);
            this.Controls.Add(this.button1);
            this.Name = "Form1";
            this.Text = "cSharpBigQuery";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.TextBox txtHoraInicio;
        private System.Windows.Forms.TextBox txtHoraFin;
        private System.Windows.Forms.ListView listCmdView;
        private System.Windows.Forms.ColumnHeader columnHeader1;
    }
}

