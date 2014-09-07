import nuke
import os

def connect_to_bookmark():
    if len(nuke.selectedNodes()) == 0:
        nuke.message('Please select a source node to connect from.')
        return

    src_node = nuke.selectedNode()
    bookmarkNodes = {}

    for n in nuke.allNodes():
        if n.knob('bookmark'):
            if n.knob('bookmark').value() == True:
                if n.Class() != "BackdropNode":
                    bookmarkNodes[n.name()] = n.knob("label").value(). \
                    replace(" ", "_")

    # bookmarkNodes.sort()

    bn_string = ""
    separator_str = "->"
    for bn in bookmarkNodes:
        bn_string = bn_string + ' ' + bn + separator_str + bookmarkNodes[bn]

    bn_string = bn_string.strip()

    p = nuke.Panel('Connect to bookmark')
    p.addEnumerationPulldown('Node to connect to:', bn_string)
    ret = p.show()

    if ret:
        n = p.value('Node to connect to:').split(separator_str)[0]
        cn = nuke.toNode(n)

        # src_node.setInput(1, cn)
        src_node.connectInput(0, cn)
        src_node.knob("label").setValue("")

        if cn.Class() == "Read":
            if src_node.Class() == "Dot":
                plate = os.path.basename(cn.knob("file").value())
                src_node.knob("label").setValue(plate)
                src_node.knob("note_font_size").setValue(30)
        else:
            if cn.knob("label"):
                cn_label = cn.knob("label").value()
                if src_node.Class() == "Dot":
                    src_node.knob("label").setValue(cn_label)
                    src_node.knob("note_font_size").setValue(30)
