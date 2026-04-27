import os
import sys
import base64
import nacl.secret
import nacl.utils

def get_secretbox():
    """Récupère la SecretBox avec la clé depuis les secrets GitHub"""
    key_b64 = os.environ.get("SECRETBOX_KEY")
    if not key_b64:
        raise ValueError("❌ SECRETBOX_KEY non trouvée dans les variables d'environnement")
    key = base64.b64decode(key_b64)
    return nacl.secret.SecretBox(key)

def encrypt_file(input_file, output_file):
    """Chiffre un fichier avec PyNaCl SecretBox"""
    box = get_secretbox()
    with open(input_file, "rb") as f:
        data = f.read()
    
    # SecretBox génère automatiquement un nonce unique
    encrypted = box.encrypt(data)
    
    with open(output_file, "wb") as f:
        f.write(encrypted)
    
    print(f"✅ Fichier chiffré (SecretBox) : {input_file} -> {output_file}")

def decrypt_file(input_file, output_file):
    """Déchiffre un fichier avec PyNaCl SecretBox"""
    box = get_secretbox()
    with open(input_file, "rb") as f:
        encrypted = f.read()
    
    try:
        decrypted = box.decrypt(encrypted)
        with open(output_file, "wb") as f:
            f.write(decrypted)
        print(f"✅ Fichier déchiffré (SecretBox) : {input_file} -> {output_file}")
    except Exception as e:
        print(f"❌ Erreur de déchiffrement : {e}")
        print("Le fichier a peut-être été modifié ou la clé est incorrecte.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python app/secretbox_crypto.py [encrypt|decrypt] input output")
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