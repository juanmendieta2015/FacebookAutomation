from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import os

load_dotenv()
post_url = os.getenv("POST_URL")
chrome_user_data = r"C:\Users\juanm\AppData\Local\Google\Chrome\User Data"
profiles = ["Profile 19", "Profile 24", "Profile 30", "Profile 31", "Profile 32", "Profile 33", "Profile 36", "Profile 37", "Profile 41", "Profile 42", "Profile 44", "Profile 46"]  

def scroll_comments():
    xpath_ver_mas_comentarios = "//span[contains(text(), 'Ver más comentarios')]"
    wait = WebDriverWait(driver, 20) 
    
    mas_relevantes = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Más relevantes"]')))
    mas_relevantes.click()        
    
    todos_los_comentarios = driver.find_element(By.XPATH, '//span[text()="Todos los comentarios"]')
    todos_los_comentarios.click()

    while True:
        try:
            ver_mas_comentarios = wait.until(
                EC.element_to_be_clickable((By.XPATH,xpath_ver_mas_comentarios))
            )     
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ver_mas_comentarios)     
            ver_mas_comentarios.click()    
            print("scrolled")
            time.sleep(2)
        except:
            print("scrolls ended")
            break
    
def like_comments():
    current_like_path = "/following::div[contains(text(), 'Me gusta')][1]"
    wait = WebDriverWait(driver, 20) 
        
    with open("datos.txt", "r", encoding="utf-8") as file:
        input_values = [line.strip() for line in file]
        
    for value in input_values:
        if value.endswith(".jpg"):
            xpath_like = f"//img[contains(@src, '{value}')]{current_like_path}"
        elif "segundos" in value:
            xpath_like = f"//div[contains(normalize-space(@aria-label), '{value}')]{current_like_path}"
        else:
            xpath_like = f"//div[contains(normalize-space(text()), '{value}')]{current_like_path}"
        try:
            reaction = wait.until(
                EC.element_to_be_clickable((By.XPATH, xpath_like))
            )     
            
            style_attribute = reaction.get_attribute("style")
            
            if not style_attribute:       
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", reaction)   
                time.sleep(1)
                reaction = wait.until(
                    EC.element_to_be_clickable((By.XPATH, xpath_like))
                )
                driver.execute_script("arguments[0].click();", reaction)
                print("Se hizo click en el boton me gusta")
                print(value)
            else:
                print("Ya está likeado, no se hizo click")
                print(value)
        except TimeoutException:
            print("No se encontró el elemento, pasando al siguiente.")
            print(value)
            continue 
        except Exception as e:
            print(f"Error inesperado: {e}")
            continue

for i, profile in enumerate(profiles, start=1):
    print(f"🟢 Abriendo Facebook con el perfil: {profile}")
    options = Options()
    options.add_argument(f"user-data-dir={chrome_user_data}")
    options.add_argument(f"profile-directory={profile}")
    options.add_argument("--headless") 
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()    
    driver.get(post_url)  
    driver.implicitly_wait(10) 
    wait = WebDriverWait(driver, 30)    
    xpath_pause = '//div[@aria-label="Pausar"]'
    
    pause = driver.find_elements(By.XPATH, xpath_pause)
    wait.until(EC.element_to_be_clickable(pause[0]))
    driver.execute_script("arguments[0].click();", pause[0])

    try:
        scroll_comments()
        like_comments()
    except Exception as e:
        print(f"Error al hacer clic en el elemento: {e}")
        
    driver.quit()  
    time.sleep(1)   # Time for waiting before changing between profiles


