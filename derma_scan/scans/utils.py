from datetime import datetime


def skin_image_upload_path(instance, filename):
    now = datetime.now().strftime('%Y/%m/%d')
    return f'SkinImages/{instance.user.id}/{now}/{filename}'