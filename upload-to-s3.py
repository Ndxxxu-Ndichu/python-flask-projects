 if location == 'kilimani':
        UPLOAD_FOLDER = f"uploads/{manager}/{location}/{property_id}"
        os.makedirs(f'{UPLOAD_FOLDER}', exist_ok=True)
        BUCKET = 'naibnb'
        files = request.files.getlist('file[]')
        for file in files:
         file.save(os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)))
         upload_file(f'{UPLOAD_FOLDER}/{file.filename}', BUCKET)
        return 'pass'
