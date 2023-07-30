from flask_admin import form 
from flask_admin.contrib.sqla import ModelView

from .utils import BASE_DIR


class ProductAdminView(ModelView):
    form_extra_fields = {
        "image1": form.ImageUploadField(
            label="Image1",
            base_path= BASE_DIR / "assets",
            relative_path="static/images/products/"
        ),
        "image2": form.ImageUploadField(
            label="Image2",
            base_path= BASE_DIR / "assets",
            relative_path="static/images/products/"
        ),
        "image3": form.ImageUploadField(
            label="Image3",
            base_path= BASE_DIR / "assets",
            relative_path="static/images/products/"
        )
    }
    
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.generate_slug()
        return super().on_model_change(form, model, is_created)