"""
Form generation and handling helpers.
"""
from typing import Any, Dict, List, Optional
from farbox_bucket.server.template_system.namespace.utils.form_utils import (
    create_simple_form as _create_simple_form,
    create_grid_form as _create_grid_form,
    create_form_dom_by_field as _create_form_dom_by_field,
    create_form_dom as _create_form_dom,
    get_data_obj_from_POST as _form_get_data_obj_from_POST
)


class FormHelper:
    """
    Helpers for form generation and processing.
    """

    @staticmethod
    def simple_form(
        title: str = '',
        keys: tuple = (),
        data_obj: Optional[Dict[str, Any]] = None,
        formats: Optional[Dict[str, Any]] = None,
        info: Optional[str] = None,
        submit_text: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """
        Create a simple form.

        Args:
            title: Form title
            keys: Field keys
            data_obj: Data object with values
            formats: Field format specifications
            info: Additional info text
            submit_text: Submit button text
            **kwargs: Additional form options

        Returns:
            HTML form
        """
        return _create_simple_form(
            title=title,
            keys=keys,
            data_obj=data_obj,
            formats=formats,
            info=info,
            submit_text=submit_text,
            **kwargs
        )

    @staticmethod
    def grid_form(
        data_obj: Optional[Dict[str, Any]] = None,
        keys: Optional[List[str]] = None,
        formats: Optional[Dict[str, Any]] = None,
        callback_func: Optional[str] = None,
        form_id: Optional[str] = None,
        ajax: bool = True,
        **kwargs: Any
    ) -> str:
        """
        Create a grid-based form layout.

        Args:
            data_obj: Data object
            keys: Form field keys
            formats: Field formats
            callback_func: JavaScript callback function
            form_id: Form DOM ID
            ajax: Enable AJAX submission
            **kwargs: Additional options

        Returns:
            HTML grid form
        """
        return _create_grid_form(
            data_obj=data_obj,
            keys=keys,
            formats=formats,
            callback_func=callback_func,
            form_id=form_id,
            ajax=ajax,
            **kwargs
        )

    @staticmethod
    def create_field_dom(field: Any, field_container_class: str = '', **kwargs: Any) -> str:
        """
        Create DOM for a single form field.

        Args:
            field: Field object
            field_container_class: Container CSS class
            **kwargs: Additional options

        Returns:
            HTML field DOM
        """
        return _create_form_dom_by_field(field, field_container_class, **kwargs)

    @staticmethod
    def create_form_dom(
        data_obj: Any,
        form_keys: Optional[List[str]] = None,
        formats: Optional[Dict[str, Any]] = None,
        form_key: Optional[str] = None
    ) -> str:
        """
        Create form DOM from data object.

        Args:
            data_obj: Data object
            form_keys: Keys to include
            formats: Field formats
            form_key: Specific form key

        Returns:
            HTML form DOM
        """
        return _create_form_dom(data_obj, form_keys, formats, form_key)

    @staticmethod
    def get_form_data(keys: List[str]) -> Dict[str, Any]:
        """
        Get form data from POST request.

        Args:
            keys: Keys to extract from POST data

        Returns:
            Dictionary of form data
        """
        return _form_get_data_obj_from_POST(keys)
