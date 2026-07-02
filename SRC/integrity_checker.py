import hashlib


def generate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(4096)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


def verify_integrity(original_file, uploaded_file):

    original_hash = generate_sha256(original_file)
    uploaded_hash = generate_sha256(uploaded_file)

    if original_hash == uploaded_hash:
        status = "Verified"
    else:
        status = "Modified"

    return original_hash, uploaded_hash, status