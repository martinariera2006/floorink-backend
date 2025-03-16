from fastapi import FastAPI, File, UploadFile
import requests
import aiofiles

app = FastAPI()

# IDs de les IA de Nyckel (CANVIA AIXÒ)
IA_ID_1 = "i2023og11aytpphq"
IA_ID_2 = "0f45t4heccgma8bj"

# Opcional: Afegir una API Key si Nyckel la requereix
API_KEY = None  # O posa None si no cal

def send_to_nyckel(file_path, ia_id, a):
    """Envia la imatge a Nyckel i retorna la resposta."""
    if a: url = f"https://www.nyckel.com/v1/functions/{ia_id}/invoke"
    else: url = f"https://www.nyckel.com/v0.9/functions/{ia_id}/invoke"

    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
    files = {"data": (file_path, open(file_path, "rb"), "image/jpeg")}
    
    response = requests.post(url, files=files, headers=headers)
    return response.json()

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    """Rep una imatge, la guarda temporalment i la processa amb les IA."""
    temp_file = f"temp_{file.filename}"
    
    async with aiofiles.open(temp_file, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    # Enviem la imatge a les dues IA
    result_ia_1 = send_to_nyckel(temp_file, IA_ID_1, True)
    result_ia_2 = send_to_nyckel(temp_file, IA_ID_2, False)

    return {
        "result_ia_1": result_ia_1,
        "result_ia_2": result_ia_2
    }

# Executa amb: uvicorn main:app --reload
