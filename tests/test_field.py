from coreali.regmodel import RegisterModel


def test_write_read(reg_desc: RegisterModel):
    reg_desc.AnAddrmap.ARegWithFields.FIELD13DOWNTO4.write(3)
    assert reg_desc.AnAddrmap.ARegWithFields.read() == 3*2**4
    assert reg_desc.AnAddrmap.ARegWithFields.FIELD13DOWNTO4.read() == 3

    reg_desc.AnAddrmap.ARepeatedReg[0].VAL.write(1)
    reg_desc.AnAddrmap.ARepeatedReg[1].VAL.write(2)
    reg_desc.AnAddrmap.ARepeatedReg[2].VAL.write(3)

    for i in range(3):
        assert reg_desc.AnAddrmap.ARepeatedReg[i].read() == i+1
    for i in range(3):
        assert reg_desc.AnAddrmap.ARepeatedReg[i].VAL.read() == i+1
