from django.utils.html import format_html
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule


@hooks.register('insert_editor_js')
def enable_source():
    return format_html(
        """
        <script>
            registerHalloPlugin('hallohtml');
        </script>
        """
    )


@hooks.register('construct_whitelister_element_rules')
def allow_iframes():
    return {
        'iframe': attribute_rule(
            {
                'src': True,
                'width': True,
                'height': True,
                'frameborder': True,
                'marginheight': True,
                'marginwidth': True
            })
    }
