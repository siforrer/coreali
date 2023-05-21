
from coreali.regmodel import Selector


def test_selectable(reg_desc):
    """
    Test is the selectable class is properly integrated
    """
    selector = Selector()
    reg_desc.AnotherAddrmap.ARepeatedReg[2]._construct_selector(
        selector.selected)
    assert selector.selected == [0, 0, 2]

    reg_desc.AnotherAddrmap.ARepeatedReg[2]._set_current_idx(
        selector.selected)
    assert reg_desc.AnotherAddrmap.ARepeatedReg.node.current_idx == [2]
    assert reg_desc.AnotherAddrmap.ARepeatedReg.node.parent.current_idx == [0]
    assert reg_desc.AnotherAddrmap.ARepeatedReg.node.parent.parent.current_idx == [
        0]


def test_selectable_with_slice(reg_desc):
    """
    Test is the selectable class is properly integrated
    """

    selector = Selector()
    reg_desc.AnAddrmap.ARegfile.ARegInARegFile._construct_selector(
        selector.selected)
    assert selector.selected == [
        0, 0, slice(0, 2, 1), slice(0, 4, 1)]

    selector = Selector()
    reg_desc.AnAddrmap.ARegfile[0].ARegInARegFile[0:3:2]._construct_selector(
        selector.selected)
    assert selector.selected == [0, 0, 0, slice(0, 3, 2)]

    selector = Selector()
    reg_desc.AnAddrmap.ARegfile[0].ARegInARegFile[2]._construct_selector(
        selector.selected)
    assert selector.selected == [0, 0, 0, 2]

    selector = Selector()
    reg_desc.AnotherAddrmap.TenRegs[2:7:2]._construct_selector(
        selector.selected)
    assert selector.selected == [0, 0, slice(2, 7, 2)]
