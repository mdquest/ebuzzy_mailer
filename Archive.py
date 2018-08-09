# -*- coding: utf-8 -*-
import io

def ReadFile(param_path):
    file = io.open(param_path, mode="r", encoding="utf-8")
    content = file.read() 
    file.close()
    return content

def Record(param_path, param_content):
    file = open(param_path, "w") 
    file.write(param_content)
    file.close() 