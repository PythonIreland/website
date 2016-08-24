from django.conf import settings
from django.utils.html import format_html, format_html_join
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule, check_url


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
            }),
        'tito-widget': attribute_rule({'event': True}),
        'tito-button': attribute_rule({'event': True}),
    }


@hooks.register('construct_whitelister_element_rules')
def allow_blockquotes():
    return {
        'a': attribute_rule({'href': check_url, 'target': True, 'class': True}),
        'blockquote': attribute_rule({'class': True}),
    }


@hooks.register('insert_editor_js')
def enable_quotes():
    js_files = [
        'js/hallo-custombuttons.js',
    ]
    js_includes = format_html_join(
        '\n',
        '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )

    return js_includes + format_html(
        """
        <script>
            registerHalloPlugin('clicktotweet');
        </script>
        """
    )


@hooks.register('insert_editor_css')
def font_awesome_css():
    return format_html('<link rel="stylesheet" href="' +
                       settings.STATIC_URL +
                       'css/font-awesome.min.css">')
