from corehq.apps.app_manager.views.app_summary import (
    AppCaseSummaryView,
    AppDataView,
    AppFormSummaryView,
    DownloadAppSummaryView,
    DownloadCaseSummaryView,
    DownloadFormSummaryView,
    FormSummaryDiffView,
)
from corehq.apps.app_manager.views.apps import (
    app_from_template,
    app_settings,
    app_source,
    copy_app,
    default_new_app,
    delete_app,
    drop_user_case,
    edit_add_ons,
    edit_app_attr,
    edit_app_langs,
    edit_app_ui_translations,
    get_app_ui_translations,
    import_app,
    new_app,
    pull_master_app,
    rearrange,
    undo_delete_app,
    update_linked_whitelist,
    view_app,
)
from corehq.apps.app_manager.views.cli import direct_ccz, list_apps
from corehq.apps.app_manager.views.download import (
    DownloadCCZ,
    download_app_strings,
    download_file,
    download_index,
    download_jad,
    download_jar,
    download_media_profile,
    download_media_suite,
    download_odk_media_profile,
    download_odk_profile,
    download_practice_user_restore,
    download_profile,
    download_raw_jar,
    download_suite,
    download_xform,
    validate_form_for_build,
)
from corehq.apps.app_manager.views.formdesigner import (
    form_source,
    form_source_legacy,
    get_form_data_schema,
)
from corehq.apps.app_manager.views.forms import (
    FormHasSubmissionsView,
    copy_form,
    delete_form,
    edit_advanced_form_actions,
    edit_form_actions,
    edit_form_attr,
    edit_form_attr_api,
    get_form_datums,
    get_form_questions,
    get_xform_source,
    new_form,
    patch_xform,
    undo_delete_form,
    view_form,
    view_form_legacy,
)
from corehq.apps.app_manager.views.modules import (
    delete_module,
    edit_module_attr,
    edit_module_detail_screens,
    edit_report_module,
    new_module,
    overwrite_module_case_list,
    undo_delete_module,
    validate_module_for_build,
    view_module,
    view_module_legacy,
)
from corehq.apps.app_manager.views.multimedia import multimedia_ajax
from corehq.apps.app_manager.views.releases import (
    AppDiffView,
    LanguageProfilesView,
    current_app_version,
    delete_copy,
    odk_install,
    odk_media_qr_code,
    odk_qr_code,
    paginate_releases,
    release_build,
    revert_to_copy,
    save_copy,
    short_odk_url,
    short_url,
    toggle_build_profile,
    update_build_comment,
)
from corehq.apps.app_manager.views.schedules import (
    edit_schedule_phases,
    edit_visit_schedule,
)
from corehq.apps.app_manager.views.settings import (
    PromptSettingsUpdateView,
    commcare_profile,
    edit_commcare_profile,
    edit_commcare_settings,
)
