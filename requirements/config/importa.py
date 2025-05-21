from ..selenium.funcoes_selenium import SeleniumAutomator
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ConfigImport():
    def __init__(self):
        self.bot = SeleniumAutomator()

    def acessar_cetip(self, empresa, user, senha, lgr):
        try:
            self.bot.navegar_para("https://nome.cetip.net.br/menu/ctp/TelaPrincipalCetip21")
            self.bot.aguardar_estado_documento()
            time.sleep(10)
            self.bot.driver.switch_to.frame("main")
            self.bot.digitar_por_xpath("/html/body/form/table/tbody/tr/td/div[2]/table/tbody/tr[2]/td[3]/input", empresa)
            self.bot.aguardar_estado_documento()
            time.sleep(2)
            self.bot.digitar_por_xpath("/html/body/form/table/tbody/tr/td/div[2]/table/tbody/tr[3]/td[3]/input", user)
            self.bot.aguardar_estado_documento()
            time.sleep(2)
            self.bot.digitar_por_xpath("/html/body/form/table/tbody/tr/td/div[2]/table/tbody/tr[4]/td[3]/input", senha)
            self.bot.aguardar_estado_documento()
            time.sleep(2)
            self.bot.clicar_por_xpath("/html/body/form/table/tbody/tr/td/div[2]/table/tbody/tr[5]/td[3]/input[1]")
            self.bot.aguardar_estado_documento()
            time.sleep(2)
            self.bot.aguardar_estado_documento()
            self.bot.driver.switch_to.default_content()
        except Exception as e:
            lgr.add_log(f"ERRO AO ABRIR PORTAL: {e}")
        
    def acessar_trans_arquivo(self, lgr):
        try:
            time.sleep(10)
            try:
                WebDriverWait(self.bot.driver, 5).until(EC.alert_is_present())
                alert = self.bot.driver.switch_to.alert
                print(f"Mensagem do alerta: {alert.text}")  # Opcional
                alert.accept()  # Clica em "OK"
            except:
                pass
            self.bot.refresh()
            self.bot.aguardar_estado_documento()
            time.sleep(2)
            self.bot.aguardar_elemento(By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/a/img")
            self.bot.clicar_por_xpath("/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/a/img")
            self.bot.aguardar_estado_documento()
            time.sleep(2)
            self.bot.aguardar_estado_documento()
            self.bot.aguardar_elemento(By.XPATH, "/html/body/div[2]/div/ul[2]/li[14]/a/span[1]")
            self.bot.clicar_por_xpath("/html/body/div[2]/div/ul[2]/li[14]/a/span[1]")
            time.sleep(2)
            self.bot.aguardar_estado_documento()
            self.bot.aguardar_elemento(By.XPATH, "/html/body/div[2]/div/ul[2]/li[14]/ul/li[1]/a/span[1]")
            self.bot.clicar_por_xpath("/html/body/div[2]/div/ul[2]/li[14]/ul/li[1]/a/span[1]")
            time.sleep(2)
            self.bot.aguardar_estado_documento()
            self.bot.aguardar_elemento(By.XPATH, "/html/body/div[2]/div/ul[2]/li[14]/ul/li[1]/ul/li[6]/a")
            self.bot.clicar_por_xpath("/html/body/div[2]/div/ul[2]/li[14]/ul/li[1]/ul/li[6]/a")
            time.sleep(2)
            self.bot.aguardar_estado_documento()
        except Exception as e:
            lgr.add_log(f"ERRO AO ACESSAR ABA DE ENVIO: {e}")
    
    def importar_layout(self, arquivo, lgr):
        try:
            time.sleep(10)
            self.bot.driver.switch_to.frame("main")
            self.bot.enviar_arquivo_por_xpath('//*[@id="file"]', arquivo)
            time.sleep(5)
            self.bot.aguardar_estado_documento()
            self.bot.clicar_por_xpath('//*[@id="uploadChooserForm"]/table/tbody/tr[2]/th/input')
            time.sleep(5)
            self.bot.aguardar_estado_documento()
            self.bot.driver.execute_script("window.print();")
            self.bot.aguardar_estado_documento()
            time.sleep(2)
            self.bot.driver.switch_to.frame("frmMenu")
            time.sleep(2)
            self.bot.clicar_por_id("btnSair")
            time.sleep(2)
            self.bot.aguardar_estado_documento()
            self.bot.fechar_navegador()
        except Exception as e:
            lgr.add_log(f"ERRO AO IMPORTAR ARQUIVO: {e}")





