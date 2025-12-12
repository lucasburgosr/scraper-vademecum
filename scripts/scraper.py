from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
action_chains = ActionChains(driver=driver)

driver.get("https://serviciosturisticos.mendoza.gov.ar/sistema/agente/")

wait = WebDriverWait(driver, 5)

usuario = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "input[type='text']")))
usuario.click()
usuario.send_keys("mguerra")
password = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "input[placeholder='Contraseña']")))
password.click()
password.send_keys("mguerra123")

submit = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "button[type='submit']"))).click()

vademecum = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "a[id='vadem']"))).click()

# ENTRA A ALOJAMIENTOS
# alojamientos_tab = wait.until(EC.element_to_be_clickable(
#     (By.CSS_SELECTOR, "tr[id='rubros_datagrid-row-r2-2-1']"))).click()

# ENTRA A AGENCIAS
alojamientos_tab = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "tr[id='rubros_datagrid-row-r2-2-0']"))).click()

paginas = 24 # 57 en alojamientos
index = 0
# alojamientos_vademecum = []

agencias_vademecum = []

try: 
    while index < paginas:

        # alojamientos = wait.until(EC.presence_of_all_elements_located(
        #     (By.XPATH, "//table[contains(@class, 'datagrid-btable')][.//tr[contains(@id, 'registros_datagrid-row')]]//tr[not(@style='background-color:#C285C2;color:#fff;')]")))

        agencias = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//table[contains(@class, 'datagrid-btable')][.//tr[contains(@id, 'registros_datagrid-row')]]//tr[not(@style='background-color:#C285C2;color:#fff;')]")))

        for agencia in agencias:

            action_chains.double_click(agencia).perform()

            time.sleep(2)

            id = wait.until(EC.presence_of_element_located(
                (By.XPATH,
                "//input[@class='textbox-value' and @name='legajo' and @type='hidden']")
            )).get_attribute("value")

            nombre = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//input[@class='textbox-value' and @name='nombre' and @type='hidden']"))).get_attribute("value")

            # habitaciones = wait.until(EC.presence_of_element_located(
            #     (By.XPATH, "//input[@class='textbox-value' and @name='cantidad_habit' and @type='hidden']"))).get_attribute("value")

            # parcelas = wait.until(EC.presence_of_element_located(
            #     (By.XPATH, "//input[@class='textbox-value' and @name='cantidad_parcelas' and @type='hidden']"))).get_attribute("value")

            # plazas = wait.until(EC.presence_of_element_located(
            #     (By.XPATH, "//input[@class='textbox-value' and @name='cantidad_plazas' and @type='hidden']"))).get_attribute("value")
            
            # cabañas = wait.until(EC.presence_of_element_located(
            #     (By.XPATH, "//input[@class='textbox-value' and @name='cantidad_cabanias' and @type='hidden']"))).get_attribute("value")

            # fecha_inscripcion = wait.until(EC.presence_of_element_located(
            #     (By.XPATH, "//input[@class='textbox-value' and @name='fecha_inscripcion' and @type='hidden']"))).get_attribute("value")

            # departamento = wait.until(EC.presence_of_element_located(
            #     (By.XPATH, "//input[@class='textbox-value' and @name='depto' and @type='hidden']"))).get_attribute("value")

            clasificacion = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//input[@class='textbox-value' and @name='clasificacion' and @type='hidden']"))).get_attribute("value") # name='clase' en alojamientos

            # localidad = wait.until(EC.presence_of_element_located(
            #     (By.XPATH, "//input[@class='textbox-value' and @name='localidad' and @type='hidden']"))).get_attribute("value")
            
            tipo = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[7]/div[2]/form/table[2]/tbody/tr[6]/td[1]/span[1]/input"))).get_attribute("value")

            agencias_vademecum.append(
                [id, nombre, clasificacion, tipo])

            cerrar = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[7]/div[1]/div[2]/a"))).click()

        index = index + 1
        paginado = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "span[class='l-btn-icon pagination-next']"))).click()
        time.sleep(1)
except: 
    pass

driver.quit()

# Guardar los datos en un archivo CSV con pandas
columnas = ["Legajo", "Nombre", "Clasificación", "Tipo"]
df = pd.DataFrame(agencias_vademecum, columns=columnas)
df.to_csv("agencias.csv", index=False, encoding="utf-8")
print("Datos guardados en 'alojamientos.csv'")
