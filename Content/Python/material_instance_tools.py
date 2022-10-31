import unreal

ATH = unreal.AssetToolsHelpers
MIC = unreal.MaterialInstanceConstant
EAL = unreal.EditorAssetLibrary
MEL = unreal.MaterialEditingLibrary
EUL = unreal.EditorUtilityLibrary
T = unreal.Texture


def create_new_material_instance_asset(name, base_material_path):
    asset_tools = ATH.get_asset_tools()
    material_instance = MIC()

    package_name, asset_name = asset_tools.create_unique_asset_name(name, '')
    if not EAL.does_asset_exist(package_name):
        path = package_name.rsplit('/', 1)[0]
        name = package_name.rsplit('/', 1)[1]
        material_instance = asset_tools.create_asset(name, path, MIC,
                                                     unreal.MaterialInstanceConstantFactoryNew())
    else:
        material_instance = unreal.load_asset(package_name)

    base_material = EAL.find_asset_data(base_material_path)
    MEL.set_material_instance_parent(material_instance, base_material.get_asset())
    return material_instance


suffix_to_parameter_map = {
    'D': 'Albedo',
    'M': 'Metalness',
    'N': 'Normal',
    'R': 'DR',
}


def create_material_instance_from_textures(name, base_material_path):
    if not base_material_path:
        # No path provided. Ask for the new base material.
        result, base_material_path = ask_for_base_material_path()
        if not result:
            # Operation canceled by user.
            return

    material_instance = create_new_material_instance_asset(name, base_material_path)

    selected_assets = EUL.get_selected_assets()
    for asset in selected_assets:
        if isinstance(asset, T):
            texture_name = asset.get_path_name()
            texture_suffix = texture_name.rsplit('_', 1)[1]
            if texture_suffix in suffix_to_parameter_map:
                parameter_name = suffix_to_parameter_map[texture_suffix]
                MEL.set_material_instance_texture_parameter_value(material_instance, parameter_name, asset)

    EAL.save_asset(material_instance.get_path_name(), only_if_is_dirty=True)

    asset_tools = ATH.get_asset_tools()
    asset_tools.open_editor_for_assets([material_instance])


def ask_for_base_material_path():
    helper_type = unreal.load_class(None,
                                    '/UtilityToolkit/MaterialTools/BP_BaseMaterialSelectDialogHelper.BP_BaseMaterialSelectDialogHelper_C')

    base_material_select_dialog_helper = unreal.new_object(helper_type)
    options = unreal.EditorDialogLibraryObjectDetailsViewOptions(show_object_name=True,
                                                                 allow_search=True)
    result = unreal.EditorDialog.show_object_details_view("Select the base material",
                                                          base_material_select_dialog_helper, options)

    base_material = base_material_select_dialog_helper.get_editor_property('Material')
    base_material_path = base_material.get_path_name()

    return result, base_material_path
