# -*- coding: utf-8 -*-

#Importando as bibliotecas
import sys  
import httplib
import urllib
import json
import string

#Importando arquivo de configuracao
import Config
import Archive
import Mailer

def GetActivities():
    try:
        params = urllib.urlencode({'hash': Config.HASH_API})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection(Config.JSON_URL, 80, timeout=500)
        conn.request("POST", "/api/tasks", params, headers)
        response = conn.getresponse()
        data = response.read()
        Archive.Record('logs/run.json' ,data)
        ProcessData(data)
        conn.close()
    except:
        print('Erro ao conectar ao microservico')

def ReadTemplate():
    return Archive.ReadFile("templates/activity.html")

def ProcessData(param_data):
    try:
        data = json.loads(param_data)

        #Carrega os usuários que vão receber os emails
        totalUser = len(data)
        countUser = 0
        while (countUser < totalUser):
            user_email = data[countUser]["email"]
            user_name =  data[countUser]["name"]

            #Carrega as atividades que serão enviadas aos usuários        
            totalActivity = len(data[countUser]["activities"])
            countActivity = 0
            
            htmlContent = ''
            
            while(countActivity < totalActivity):
                description = data[countUser]["activities"][countActivity]["description"]
                name = data[countUser]["activities"][countActivity]["name"]
                project = data[countUser]["activities"][countActivity]["project"]
                sprint = data[countUser]["activities"][countActivity]["sprint"]

                htmlContent = ''.join([
                    htmlContent,
                    '<tr>',
                    "<td style='border-top: 1px solid #e4e7ea; padding: 15px 8px;'>", str(countActivity + 1), '</td>',
                    "<td style='border-top: 1px solid #e4e7ea; padding: 15px 8px;'>", project, '</td>',
                    "<td style='border-top: 1px solid #e4e7ea; padding: 15px 8px;'>", sprint, '</td>',
                    "<td style='border-top: 1px solid #e4e7ea; padding: 15px 8px;'>", name, '</td>',
                    '</tr>'
                ])
  
                countActivity = countActivity + 1
            #endwhile
            template = ReadTemplate()
            template = string.replace(template, "@usuario", user_name)
            template = string.replace(template, "@htmlContent", htmlContent)
            
            if(totalActivity  > 0):
                Mailer.SendHTML("Atividades pendentes", template, user_email)
            #endif
            
            del(htmlContent)
            countUser =  countUser + 1 
        #endwhile    
    except:
        print("Erro ao dar parse no json")

GetActivities()