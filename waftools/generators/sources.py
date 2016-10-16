from waflib.Build import BuildContext
import os

def __file2string_cmd__(ctx):
    return '"${{BIN_PERL}}" "{0}/TOOLS/file2string.pl" "${{SRC}}" > "${{TGT}}"' \
                .format(ctx.srcnode.abspath())

def __matroska_cmd__(ctx, argument):
    return '"${{BIN_PERL}}" "{0}/TOOLS/matroska.pl" "{1}" "${{SRC}}" > "${{TGT}}"' \
                .format(ctx.srcnode.abspath(), argument)

def __zshcomp_cmd__(ctx, argument):
    return '"${{BIN_PERL}}" "{0}/TOOLS/zsh.pl" "{1}" > "${{TGT}}"' \
                .format(ctx.srcnode.abspath(), argument)

def __wayland_scanner_cmd__(ctx, argument):
    return "${{WAYSCAN}} {0} < ${{SRC}} > ${{TGT}}".format(argument)

def __file2string__(ctx, **kwargs):
    ctx(
        rule   = __file2string_cmd__(ctx),
        before = ("c",),
        name   = os.path.basename(kwargs['target']),
        **kwargs
    )

def __matroska_header__(ctx, **kwargs):
    ctx(
        rule   = __matroska_cmd__(ctx, '--generate-header'),
        before = ("c",),
        name   = os.path.basename(kwargs['target']),
        **kwargs
    )

def __matroska_definitions__(ctx, **kwargs):
    ctx(
        rule   = __matroska_cmd__(ctx, '--generate-definitions'),
        before = ("c",),
        **kwargs
    )

def __zshcomp__(ctx, **kwargs):
    ctx(
        rule   = __zshcomp_cmd__(ctx, ctx.bldnode.abspath() + '/mpv'),
        after = ("c", "cprogram",),
        name   = os.path.basename(kwargs['target']),
        **kwargs
    )

def __wayland_protocol_code__(ctx, **kwargs):
    ctx(
        rule   = __wayland_scanner_cmd__(ctx, 'code'),
        name   = os.path.basename(kwargs['target']),
        **kwargs
    )

def __wayland_protocol_header__(ctx, **kwargs):
    ctx(
        rule   = __wayland_scanner_cmd__(ctx, 'client-header'),
        before = ('c',),
        name   = os.path.basename(kwargs['target']),
        **kwargs
    )

BuildContext.file2string             = __file2string__
BuildContext.matroska_header         = __matroska_header__
BuildContext.matroska_definitions    = __matroska_definitions__
BuildContext.wayland_protocol_code   = __wayland_protocol_code__
BuildContext.wayland_protocol_header = __wayland_protocol_header__
BuildContext.zshcomp                 = __zshcomp__
