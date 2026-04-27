import os
import sys
from cryptography.fernet import Fernet

def get_fernet():
    """Récupère la clé Fernet depuis les secrets GitHub"""
    key = os.environ.get("FERNET_KEY")
    if not key:
        raise ValueError("❌ FERNET_KEY non trouvée dans les variables d'environnement")
    return Fernet(key.encode())

def encrypt_file(input_file, output_file):
    """Chiffre un fichier avec Fernet"""
    f = get_fernet()
    with open(input_file, "rb") as file:
        data = file.read()
    encrypted = f.encrypt(data)
    with open(output_file, "wb") as file:
        file.write(encrypted)
    print(f"✅ Fichier chiffré (Fernet) : {input_file} -> {output_file}")

def decrypt_file(input_file, output_file):
    """Déchiffre un fichier avec Fernet"""
    f = get_fernet()
    with open(input_file, "rb") as file:
        data = file.read()
    try:
        decrypted = f.decrypt(data)
        with open(output_file, "wb") as file:
            file.write(decrypted)
        print(f"✅ Fichier déchiffré (Fernet) : {input_file} -> {output_file}")
    except Exception as e:
        print(f"❌ Erreur de déchiffrement : {e}")
        print("Le fichier a peut-être été modifié ou la clé est incorrecte.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python app/fernet_atelier1.py [encrypt|decrypt] input output")
        sys.exit(1)

    action = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if action == "encrypt":
        encrypt_file(input_file, output_file)
    elif action == "decrypt":
        decrypt_file(input_file, output_file)
    else:
        print("❌ Action invalide : utilisez 'encrypt' ou 'decrypt'")
        sys.exit(1)