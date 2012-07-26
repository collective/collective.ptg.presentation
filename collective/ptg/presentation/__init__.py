from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.plonetruegallery import PTGMessageFactory as _
from collective.plonetruegallery.browser.views.display import \
    BatchingDisplayType
from collective.plonetruegallery.interfaces import IBaseSettings
from zope import schema


class IPresentationDisplaySettings(IBaseSettings):
    presentation_effect = schema.Choice(
        title=_(u"label_presentation_effect",
            default=u"Mouseover or click"),
        default="click",
        vocabulary=SimpleVocabulary([
            SimpleTerm("click", "click",
                _(u"label_presentation_click", default=u"Click on image")),
            SimpleTerm("mouseenter", "mouseenter",
                _(u"label_presentation_mouseover", default=u"Mouse enter")
            )
        ]))
    presentation_width = schema.Int(
        title=_(u"label_presentation_width",
            default=u"Width of the gallery in pixels"),
        default=600,
        min=200)
    presentation_height = schema.Int(
        title=_(u"label_presentation_height",
            default=u"Height of the gallery in pixels"),
        default=350,
        min=60)
    minimum_width = schema.Int(
        title=_(u"label_presentation_minimum_width",
            default=u"Minimum width of images"),
        default=15)
    presentation_xposition = schema.Choice(
        title=_(u"label_presentation_xposition",
            default=u"Horizontal image position"),
        default="center",
        vocabulary=SimpleVocabulary([
            SimpleTerm("top", "top",
                _(u"label_presentation_xpositiontop", default=u"Top")),
            SimpleTerm("center", "center",
                _(u"label_presentation_xpositioncenter", default=u"Center")),
            SimpleTerm("bottom", "bottom",
                _(u"label_presentation_xpositionbottom", default=u"Bottom")
            )
        ]))
    presentation_yposition = schema.Choice(
        title=_(u"label_presentation_yposition",
            default=u"Vertical image position"),
        default="center",
        vocabulary=SimpleVocabulary([
            SimpleTerm("left", "left",
                _(u"label_presentation_ypositionleft", default=u"Left")),
            SimpleTerm("center", "center",
                _(u"label_presentation_ypositioncenter", default=u"Center")),
            SimpleTerm("right", "right",
                _(u"label_presentation_ypositionright", default=u"Right")
            )
        ]))
    presentation_hidetext = schema.Bool(
        title=_(u"label_presentation_hidetext",
            default=u"Hide image text"),
        default=False,
        )


class PresentationDisplayType(BatchingDisplayType):
    name = u"presentation"
    schema = IPresentationDisplaySettings
    description = _(u"label_presentation_display_type",
        default=u"Presentation")
    staticFilesRelative = '++resource++ptg.presentation'

    def javascript(self):
        imagecount = len(self.adapter.cooked_images)
        if imagecount == 0:
            imagecount = 1
        return u"""
<script type="text/javascript" charset="utf-8">
$(document).ready(function() {
    $(".presentationWrapper li").bind ({
        %(effect)s: function(){
            $(".presentationWrapper li").addClass("unpresented");
            $(this).addClass("presented").removeClass("unpresented");
            $(".unpresented").stop().animate({
                width: '%(minimum_width)ipx',
            }, 600);
            $(this).stop().animate({
                width: '%(imagelargewidth)ipx',
            }, 600);
        }
    });
    $(".presentationWrapper ul").bind ({
        mouseleave: function(){
            $(".presentationWrapper li").removeClass("unpresented presented");
            $(".presentationWrapper li").stop().animate({
                width: '%(imagewidth)ipx',
            }, 600);
        }
    });
});
</script>
""" % {
        'imagewidth': (self.settings.presentation_width - imagecount + 1) /
                        imagecount,
        'imagelargewidth': self.settings.presentation_width -
            ((imagecount - 1) * self.settings.minimum_width) - imagecount + 1,
        'effect': self.settings.presentation_effect,
        'minimum_width': self.settings.minimum_width
    }

    def css(self):
        imagecount = len(self.adapter.cooked_images)
        if imagecount == 0:
            imagecount = 1
        return u"""
<link rel="stylesheet" type="text/css"
    href="%(base_url)s/style.css"/>
    <style>
.presentationWrapper {
    width: %(width)ipx;
    height: %(height)ipx;
}

.presentationWrapper li  {
    width: %(imagewidth)ipx;
    height: %(height)ipx;
    background-position: %(xposition)s %(yposition)s;
}

li.row_%(lastimagenr)s div.presentationshadow {
    background-image: none;
}
</style>
""" % {
        'base_url': self.staticFiles,
        'height': self.settings.presentation_height,
        'width': self.settings.presentation_width,
        'xposition': self.settings.presentation_xposition,
        'yposition': self.settings.presentation_yposition,
        'lastimagenr': imagecount - 1,
        'imagewidth': (self.settings.presentation_width - imagecount + 1) /
                        imagecount
    }
PresentationSettings = createSettingsFactory(PresentationDisplayType.schema)
