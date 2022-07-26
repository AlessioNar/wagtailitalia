from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.fields import StreamField
from wagtail.documents.blocks import DocumentChooserBlock

class Color(blocks.StructBlock):    
    """A color palette"""
    primary = blocks.CharBlock(max_length=7, default="#FFFFFF", 
        help_text="Add an exadecimal color code: #FFFFFF for white")    
    secondary = blocks.CharBlock(max_length=7, default="#FFFFFF", 
        help_text="Add an exadecimal color code: #FFFFFF for white")    
    dark = blocks.CharBlock(max_length=7, default="#FFFFFF", 
        help_text="Add an exadecimal color code: #FFFFFF for white")    
    light = blocks.CharBlock(max_length=7, default="#FFFFFF", 
        help_text="Add an exadecimal color code: #FFFFFF for white")    
    danger = blocks.CharBlock(max_length=7, default="#FFFFFF", 
        help_text="Add an exadecimal color code: #FFFFFF for white")    
    success = blocks.CharBlock(max_length=7, default="#FFFFFF", 
        help_text="Add an exadecimal color code: #FFFFFF for white")    
    warning = blocks.CharBlock(max_length=7, default="#FFFFFF", 
        help_text="Add an exadecimal color code: #FFFFFF for white")    
            
    class Meta: # noqa
        template = "streams/title_block.html"
        icon = "edit"
        label = "Title"