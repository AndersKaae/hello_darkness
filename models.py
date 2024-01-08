class ImageClass:
    crop_pos: dict[int,int] = {"x":"","y":""}
    crop_dimensions: dict[int,int] = {"height":"","width":""}
    original_image_dimenions: dict[int,int] = {"height":"","width":""}
    reduced_image_dimensions: dict[int,int] = {"height":"","width":""}
    file_name: str = ""
    file_extension: str = ""
    total_images: int = 0

    def reduced_to_original_factor(self):
        return self.original_image_dimenions['width'] / self.reduced_image_dimensions['width']

    def full_file_name(self):
        return self.file_name + "." + self.file_extension

    def tmp_folder(self):
        return 'static/user_uploads/'+ self.file_name + '/' # static/user_uploads/d3c194ce-f564-497d-bb82-0f7232503640/
