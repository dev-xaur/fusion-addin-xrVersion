import adsk.core, adsk.fusion

handlers = []


def update_version():
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    if not design:
        return

    doc = app.activeDocument
    version = doc.dataFile.versionNumber

    params = design.userParameters
    name = "xrVersion"

    p = params.itemByName(name)
    if p:
        p.expression = str(version)
    else:
        params.add(
            name,
            adsk.core.ValueInput.createByString(str(version)),
            "",
            "xrVersion add-in: Automatic file versioning",
        )


class DocActivatedHandler(adsk.core.DocumentEventHandler):
    def notify(self, args):
        update_version()


def run(context):
    app = adsk.core.Application.get()
    handler = DocActivatedHandler()
    app.documentActivated.add(handler)
    handlers.append(handler)


def stop(context):
    handlers.clear()
