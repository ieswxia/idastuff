# Print ARM64_SYSREG using symbolic names.
#
# Copyright (c) 2017 xerub.  All rights reserved

import idautils
import idaapi
import idc

import traceback

hexnight_cb_info = None
hexnight_cb = None

# generated from capstone/arch/AArch64/AArch64BaseInfo.h
regs = {
                                  # Op0 Op1  CRn   CRm   Op2
    0x9808 : "MDCCSR_EL0",        # 10  011  0000  0001  000
    0x9828 : "DBGDTRRX_EL0",      # 10  011  0000  0101  000
    0x8080 : "MDRAR_EL1",         # 10  000  0001  0000  000
    0x808c : "OSLSR_EL1",         # 10  000  0001  0001  100
    0x83f6 : "DBGAUTHSTATUS_EL1", # 10  000  0111  1110  110
    0xdce6 : "PMCEID0_EL0",       # 11  011  1001  1100  110
    0xdce7 : "PMCEID1_EL0",       # 11  011  1001  1100  111
    0xc000 : "MIDR_EL1",          # 11  000  0000  0000  000
    0xc800 : "CCSIDR_EL1",        # 11  001  0000  0000  000
    0xc801 : "CLIDR_EL1",         # 11  001  0000  0000  001
    0xd801 : "CTR_EL0",           # 11  011  0000  0000  001
    0xc005 : "MPIDR_EL1",         # 11  000  0000  0000  101
    0xc006 : "REVIDR_EL1",        # 11  000  0000  0000  110
    0xc807 : "AIDR_EL1",          # 11  001  0000  0000  111
    0xd807 : "DCZID_EL0",         # 11  011  0000  0000  111
    0xc008 : "ID_PFR0_EL1",       # 11  000  0000  0001  000
    0xc009 : "ID_PFR1_EL1",       # 11  000  0000  0001  001
    0xc00a : "ID_DFR0_EL1",       # 11  000  0000  0001  010
    0xc00b : "ID_AFR0_EL1",       # 11  000  0000  0001  011
    0xc00c : "ID_MMFR0_EL1",      # 11  000  0000  0001  100
    0xc00d : "ID_MMFR1_EL1",      # 11  000  0000  0001  101
    0xc00e : "ID_MMFR2_EL1",      # 11  000  0000  0001  110
    0xc00f : "ID_MMFR3_EL1",      # 11  000  0000  0001  111
    0xc010 : "ID_ISAR0_EL1",      # 11  000  0000  0010  000
    0xc011 : "ID_ISAR1_EL1",      # 11  000  0000  0010  001
    0xc012 : "ID_ISAR2_EL1",      # 11  000  0000  0010  010
    0xc013 : "ID_ISAR3_EL1",      # 11  000  0000  0010  011
    0xc014 : "ID_ISAR4_EL1",      # 11  000  0000  0010  100
    0xc015 : "ID_ISAR5_EL1",      # 11  000  0000  0010  101
    0xc020 : "ID_A64PFR0_EL1",    # 11  000  0000  0100  000
    0xc021 : "ID_A64PFR1_EL1",    # 11  000  0000  0100  001
    0xc028 : "ID_A64DFR0_EL1",    # 11  000  0000  0101  000
    0xc029 : "ID_A64DFR1_EL1",    # 11  000  0000  0101  001
    0xc02c : "ID_A64AFR0_EL1",    # 11  000  0000  0101  100
    0xc02d : "ID_A64AFR1_EL1",    # 11  000  0000  0101  101
    0xc030 : "ID_A64ISAR0_EL1",   # 11  000  0000  0110  000
    0xc031 : "ID_A64ISAR1_EL1",   # 11  000  0000  0110  001
    0xc038 : "ID_A64MMFR0_EL1",   # 11  000  0000  0111  000
    0xc039 : "ID_A64MMFR1_EL1",   # 11  000  0000  0111  001
    0xc018 : "MVFR0_EL1",         # 11  000  0000  0011  000
    0xc019 : "MVFR1_EL1",         # 11  000  0000  0011  001
    0xc01a : "MVFR2_EL1",         # 11  000  0000  0011  010
    0xc601 : "RVBAR_EL1",         # 11  000  1100  0000  001
    0xe601 : "RVBAR_EL2",         # 11  100  1100  0000  001
    0xf601 : "RVBAR_EL3",         # 11  110  1100  0000  001
    0xc608 : "ISR_EL1",           # 11  000  1100  0001  000
    0xdf01 : "CNTPCT_EL0",        # 11  011  1110  0000  001
    0xdf02 : "CNTVCT_EL0",        # 11  011  1110  0000  010
    0x8818 : "TRCSTATR",          # 10  001  0000  0011  000
    0x8806 : "TRCIDR8",           # 10  001  0000  0000  110
    0x880e : "TRCIDR9",           # 10  001  0000  0001  110
    0x8816 : "TRCIDR10",          # 10  001  0000  0010  110
    0x881e : "TRCIDR11",          # 10  001  0000  0011  110
    0x8826 : "TRCIDR12",          # 10  001  0000  0100  110
    0x882e : "TRCIDR13",          # 10  001  0000  0101  110
    0x8847 : "TRCIDR0",           # 10  001  0000  1000  111
    0x884f : "TRCIDR1",           # 10  001  0000  1001  111
    0x8857 : "TRCIDR2",           # 10  001  0000  1010  111
    0x885f : "TRCIDR3",           # 10  001  0000  1011  111
    0x8867 : "TRCIDR4",           # 10  001  0000  1100  111
    0x886f : "TRCIDR5",           # 10  001  0000  1101  111
    0x8877 : "TRCIDR6",           # 10  001  0000  1110  111
    0x887f : "TRCIDR7",           # 10  001  0000  1111  111
    0x888c : "TRCOSLSR",          # 10  001  0001  0001  100
    0x88ac : "TRCPDSR",           # 10  001  0001  0101  100
    0x8bd6 : "TRCDEVAFF0",        # 10  001  0111  1010  110
    0x8bde : "TRCDEVAFF1",        # 10  001  0111  1011  110
    0x8bee : "TRCLSR",            # 10  001  0111  1101  110
    0x8bf6 : "TRCAUTHSTATUS",     # 10  001  0111  1110  110
    0x8bfe : "TRCDEVARCH",        # 10  001  0111  1111  110
    0x8b97 : "TRCDEVID",          # 10  001  0111  0010  111
    0x8b9f : "TRCDEVTYPE",        # 10  001  0111  0011  111
    0x8ba7 : "TRCPIDR4",          # 10  001  0111  0100  111
    0x8baf : "TRCPIDR5",          # 10  001  0111  0101  111
    0x8bb7 : "TRCPIDR6",          # 10  001  0111  0110  111
    0x8bbf : "TRCPIDR7",          # 10  001  0111  0111  111
    0x8bc7 : "TRCPIDR0",          # 10  001  0111  1000  111
    0x8bcf : "TRCPIDR1",          # 10  001  0111  1001  111
    0x8bd7 : "TRCPIDR2",          # 10  001  0111  1010  111
    0x8bdf : "TRCPIDR3",          # 10  001  0111  1011  111
    0x8be7 : "TRCCIDR0",          # 10  001  0111  1100  111
    0x8bef : "TRCCIDR1",          # 10  001  0111  1101  111
    0x8bf7 : "TRCCIDR2",          # 10  001  0111  1110  111
    0x8bff : "TRCCIDR3",          # 10  001  0111  1111  111
    0xc660 : "ICC_IAR1_EL1",      # 11  000  1100  1100  000
    0xc640 : "ICC_IAR0_EL1",      # 11  000  1100  1000  000
    0xc662 : "ICC_HPPIR1_EL1",    # 11  000  1100  1100  010
    0xc642 : "ICC_HPPIR0_EL1",    # 11  000  1100  1000  010
    0xc65b : "ICC_RPR_EL1",       # 11  000  1100  1011  011
    0xe659 : "ICH_VTR_EL2",       # 11  100  1100  1011  001
    0xe65b : "ICH_EISR_EL2",      # 11  100  1100  1011  011
    0xe65d : "ICH_ELSR_EL2",      # 11  100  1100  1011  101
    0x9828 : "DBGDTRTX_EL0",      # 10  011  0000  0101  000
    0x8084 : "OSLAR_EL1",         # 10  000  0001  0000  100
    0xdce4 : "PMSWINC_EL0",       # 11  011  1001  1100  100
    0x8884 : "TRCOSLAR",          # 10  001  0001  0000  100
    0x8be6 : "TRCLAR",            # 10  001  0111  1100  110
    0xc661 : "ICC_EOIR1_EL1",     # 11  000  1100  1100  001
    0xc641 : "ICC_EOIR0_EL1",     # 11  000  1100  1000  001
    0xc659 : "ICC_DIR_EL1",       # 11  000  1100  1011  001
    0xc65d : "ICC_SGI1R_EL1",     # 11  000  1100  1011  101
    0xc65e : "ICC_ASGI1R_EL1",    # 11  000  1100  1011  110
    0xc65f : "ICC_SGI0R_EL1",     # 11  000  1100  1011  111
    0x8002 : "OSDTRRX_EL1",       # 10  000  0000  0000  010
    0x801a : "OSDTRTX_EL1",       # 10  000  0000  0011  010
    0x9000 : "TEECR32_EL1",       # 10  010  0000  0000  000
    0x8010 : "MDCCINT_EL1",       # 10  000  0000  0010  000
    0x8012 : "MDSCR_EL1",         # 10  000  0000  0010  010
    0x9820 : "DBGDTR_EL0",        # 10  011  0000  0100  000
    0x8032 : "OSECCR_EL1",        # 10  000  0000  0110  010
    0xa038 : "DBGVCR32_EL2",      # 10  100  0000  0111  000
    0x8004 : "DBGBVR0_EL1",       # 10  000  0000  0000  100
    0x800c : "DBGBVR1_EL1",       # 10  000  0000  0001  100
    0x8014 : "DBGBVR2_EL1",       # 10  000  0000  0010  100
    0x801c : "DBGBVR3_EL1",       # 10  000  0000  0011  100
    0x8024 : "DBGBVR4_EL1",       # 10  000  0000  0100  100
    0x802c : "DBGBVR5_EL1",       # 10  000  0000  0101  100
    0x8034 : "DBGBVR6_EL1",       # 10  000  0000  0110  100
    0x803c : "DBGBVR7_EL1",       # 10  000  0000  0111  100
    0x8044 : "DBGBVR8_EL1",       # 10  000  0000  1000  100
    0x804c : "DBGBVR9_EL1",       # 10  000  0000  1001  100
    0x8054 : "DBGBVR10_EL1",      # 10  000  0000  1010  100
    0x805c : "DBGBVR11_EL1",      # 10  000  0000  1011  100
    0x8064 : "DBGBVR12_EL1",      # 10  000  0000  1100  100
    0x806c : "DBGBVR13_EL1",      # 10  000  0000  1101  100
    0x8074 : "DBGBVR14_EL1",      # 10  000  0000  1110  100
    0x807c : "DBGBVR15_EL1",      # 10  000  0000  1111  100
    0x8005 : "DBGBCR0_EL1",       # 10  000  0000  0000  101
    0x800d : "DBGBCR1_EL1",       # 10  000  0000  0001  101
    0x8015 : "DBGBCR2_EL1",       # 10  000  0000  0010  101
    0x801d : "DBGBCR3_EL1",       # 10  000  0000  0011  101
    0x8025 : "DBGBCR4_EL1",       # 10  000  0000  0100  101
    0x802d : "DBGBCR5_EL1",       # 10  000  0000  0101  101
    0x8035 : "DBGBCR6_EL1",       # 10  000  0000  0110  101
    0x803d : "DBGBCR7_EL1",       # 10  000  0000  0111  101
    0x8045 : "DBGBCR8_EL1",       # 10  000  0000  1000  101
    0x804d : "DBGBCR9_EL1",       # 10  000  0000  1001  101
    0x8055 : "DBGBCR10_EL1",      # 10  000  0000  1010  101
    0x805d : "DBGBCR11_EL1",      # 10  000  0000  1011  101
    0x8065 : "DBGBCR12_EL1",      # 10  000  0000  1100  101
    0x806d : "DBGBCR13_EL1",      # 10  000  0000  1101  101
    0x8075 : "DBGBCR14_EL1",      # 10  000  0000  1110  101
    0x807d : "DBGBCR15_EL1",      # 10  000  0000  1111  101
    0x8006 : "DBGWVR0_EL1",       # 10  000  0000  0000  110
    0x800e : "DBGWVR1_EL1",       # 10  000  0000  0001  110
    0x8016 : "DBGWVR2_EL1",       # 10  000  0000  0010  110
    0x801e : "DBGWVR3_EL1",       # 10  000  0000  0011  110
    0x8026 : "DBGWVR4_EL1",       # 10  000  0000  0100  110
    0x802e : "DBGWVR5_EL1",       # 10  000  0000  0101  110
    0x8036 : "DBGWVR6_EL1",       # 10  000  0000  0110  110
    0x803e : "DBGWVR7_EL1",       # 10  000  0000  0111  110
    0x8046 : "DBGWVR8_EL1",       # 10  000  0000  1000  110
    0x804e : "DBGWVR9_EL1",       # 10  000  0000  1001  110
    0x8056 : "DBGWVR10_EL1",      # 10  000  0000  1010  110
    0x805e : "DBGWVR11_EL1",      # 10  000  0000  1011  110
    0x8066 : "DBGWVR12_EL1",      # 10  000  0000  1100  110
    0x806e : "DBGWVR13_EL1",      # 10  000  0000  1101  110
    0x8076 : "DBGWVR14_EL1",      # 10  000  0000  1110  110
    0x807e : "DBGWVR15_EL1",      # 10  000  0000  1111  110
    0x8007 : "DBGWCR0_EL1",       # 10  000  0000  0000  111
    0x800f : "DBGWCR1_EL1",       # 10  000  0000  0001  111
    0x8017 : "DBGWCR2_EL1",       # 10  000  0000  0010  111
    0x801f : "DBGWCR3_EL1",       # 10  000  0000  0011  111
    0x8027 : "DBGWCR4_EL1",       # 10  000  0000  0100  111
    0x802f : "DBGWCR5_EL1",       # 10  000  0000  0101  111
    0x8037 : "DBGWCR6_EL1",       # 10  000  0000  0110  111
    0x803f : "DBGWCR7_EL1",       # 10  000  0000  0111  111
    0x8047 : "DBGWCR8_EL1",       # 10  000  0000  1000  111
    0x804f : "DBGWCR9_EL1",       # 10  000  0000  1001  111
    0x8057 : "DBGWCR10_EL1",      # 10  000  0000  1010  111
    0x805f : "DBGWCR11_EL1",      # 10  000  0000  1011  111
    0x8067 : "DBGWCR12_EL1",      # 10  000  0000  1100  111
    0x806f : "DBGWCR13_EL1",      # 10  000  0000  1101  111
    0x8077 : "DBGWCR14_EL1",      # 10  000  0000  1110  111
    0x807f : "DBGWCR15_EL1",      # 10  000  0000  1111  111
    0x9080 : "TEEHBR32_EL1",      # 10  010  0001  0000  000
    0x809c : "OSDLR_EL1",         # 10  000  0001  0011  100
    0x80a4 : "DBGPRCR_EL1",       # 10  000  0001  0100  100
    0x83c6 : "DBGCLAIMSET_EL1",   # 10  000  0111  1000  110
    0x83ce : "DBGCLAIMCLR_EL1",   # 10  000  0111  1001  110
    0xd000 : "CSSELR_EL1",        # 11  010  0000  0000  000
    0xe000 : "VPIDR_EL2",         # 11  100  0000  0000  000
    0xe005 : "VMPIDR_EL2",        # 11  100  0000  0000  101
    0xc082 : "CPACR_EL1",         # 11  000  0001  0000  010
    0xc080 : "SCTLR_EL1",         # 11  000  0001  0000  000
    0xe080 : "SCTLR_EL2",         # 11  100  0001  0000  000
    0xf080 : "SCTLR_EL3",         # 11  110  0001  0000  000
    0xc081 : "ACTLR_EL1",         # 11  000  0001  0000  001
    0xe081 : "ACTLR_EL2",         # 11  100  0001  0000  001
    0xf081 : "ACTLR_EL3",         # 11  110  0001  0000  001
    0xe088 : "HCR_EL2",           # 11  100  0001  0001  000
    0xf088 : "SCR_EL3",           # 11  110  0001  0001  000
    0xe089 : "MDCR_EL2",          # 11  100  0001  0001  001
    0xf089 : "SDER32_EL3",        # 11  110  0001  0001  001
    0xe08a : "CPTR_EL2",          # 11  100  0001  0001  010
    0xf08a : "CPTR_EL3",          # 11  110  0001  0001  010
    0xe08b : "HSTR_EL2",          # 11  100  0001  0001  011
    0xe08f : "HACR_EL2",          # 11  100  0001  0001  111
    0xf099 : "MDCR_EL3",          # 11  110  0001  0011  001
    0xc100 : "TTBR0_EL1",         # 11  000  0010  0000  000
    0xe100 : "TTBR0_EL2",         # 11  100  0010  0000  000
    0xf100 : "TTBR0_EL3",         # 11  110  0010  0000  000
    0xc101 : "TTBR1_EL1",         # 11  000  0010  0000  001
    0xc102 : "TCR_EL1",           # 11  000  0010  0000  010
    0xe102 : "TCR_EL2",           # 11  100  0010  0000  010
    0xf102 : "TCR_EL3",           # 11  110  0010  0000  010
    0xe108 : "VTTBR_EL2",         # 11  100  0010  0001  000
    0xe10a : "VTCR_EL2",          # 11  100  0010  0001  010
    0xe180 : "DACR32_EL2",        # 11  100  0011  0000  000
    0xc200 : "SPSR_EL1",          # 11  000  0100  0000  000
    0xe200 : "SPSR_EL2",          # 11  100  0100  0000  000
    0xf200 : "SPSR_EL3",          # 11  110  0100  0000  000
    0xc201 : "ELR_EL1",           # 11  000  0100  0000  001
    0xe201 : "ELR_EL2",           # 11  100  0100  0000  001
    0xf201 : "ELR_EL3",           # 11  110  0100  0000  001
    0xc208 : "SP_EL0",            # 11  000  0100  0001  000
    0xe208 : "SP_EL1",            # 11  100  0100  0001  000
    0xf208 : "SP_EL2",            # 11  110  0100  0001  000
    0xc210 : "SPSel",             # 11  000  0100  0010  000
    0xda10 : "NZCV",              # 11  011  0100  0010  000
    0xda11 : "DAIF",              # 11  011  0100  0010  001
    0xc212 : "CurrentEL",         # 11  000  0100  0010  010
    0xe218 : "SPSR_irq",          # 11  100  0100  0011  000
    0xe219 : "SPSR_abt",          # 11  100  0100  0011  001
    0xe21a : "SPSR_und",          # 11  100  0100  0011  010
    0xe21b : "SPSR_fiq",          # 11  100  0100  0011  011
    0xda20 : "FPCR",              # 11  011  0100  0100  000
    0xda21 : "FPSR",              # 11  011  0100  0100  001
    0xda28 : "DSPSR_EL0",         # 11  011  0100  0101  000
    0xda29 : "DLR_EL0",           # 11  011  0100  0101  001
    0xe281 : "IFSR32_EL2",        # 11  100  0101  0000  001
    0xc288 : "AFSR0_EL1",         # 11  000  0101  0001  000
    0xe288 : "AFSR0_EL2",         # 11  100  0101  0001  000
    0xf288 : "AFSR0_EL3",         # 11  110  0101  0001  000
    0xc289 : "AFSR1_EL1",         # 11  000  0101  0001  001
    0xe289 : "AFSR1_EL2",         # 11  100  0101  0001  001
    0xf289 : "AFSR1_EL3",         # 11  110  0101  0001  001
    0xc290 : "ESR_EL1",           # 11  000  0101  0010  000
    0xe290 : "ESR_EL2",           # 11  100  0101  0010  000
    0xf290 : "ESR_EL3",           # 11  110  0101  0010  000
    0xe298 : "FPEXC32_EL2",       # 11  100  0101  0011  000
    0xc300 : "FAR_EL1",           # 11  000  0110  0000  000
    0xe300 : "FAR_EL2",           # 11  100  0110  0000  000
    0xf300 : "FAR_EL3",           # 11  110  0110  0000  000
    0xe304 : "HPFAR_EL2",         # 11  100  0110  0000  100
    0xc3a0 : "PAR_EL1",           # 11  000  0111  0100  000
    0xdce0 : "PMCR_EL0",          # 11  011  1001  1100  000
    0xdce1 : "PMCNTENSET_EL0",    # 11  011  1001  1100  001
    0xdce2 : "PMCNTENCLR_EL0",    # 11  011  1001  1100  010
    0xdce3 : "PMOVSCLR_EL0",      # 11  011  1001  1100  011
    0xdce5 : "PMSELR_EL0",        # 11  011  1001  1100  101
    0xdce8 : "PMCCNTR_EL0",       # 11  011  1001  1101  000
    0xdce9 : "PMXEVTYPER_EL0",    # 11  011  1001  1101  001
    0xdcea : "PMXEVCNTR_EL0",     # 11  011  1001  1101  010
    0xdcf0 : "PMUSERENR_EL0",     # 11  011  1001  1110  000
    0xc4f1 : "PMINTENSET_EL1",    # 11  000  1001  1110  001
    0xc4f2 : "PMINTENCLR_EL1",    # 11  000  1001  1110  010
    0xdcf3 : "PMOVSSET_EL0",      # 11  011  1001  1110  011
    0xc510 : "MAIR_EL1",          # 11  000  1010  0010  000
    0xe510 : "MAIR_EL2",          # 11  100  1010  0010  000
    0xf510 : "MAIR_EL3",          # 11  110  1010  0010  000
    0xc518 : "AMAIR_EL1",         # 11  000  1010  0011  000
    0xe518 : "AMAIR_EL2",         # 11  100  1010  0011  000
    0xf518 : "AMAIR_EL3",         # 11  110  1010  0011  000
    0xc600 : "VBAR_EL1",          # 11  000  1100  0000  000
    0xe600 : "VBAR_EL2",          # 11  100  1100  0000  000
    0xf600 : "VBAR_EL3",          # 11  110  1100  0000  000
    0xc602 : "RMR_EL1",           # 11  000  1100  0000  010
    0xe602 : "RMR_EL2",           # 11  100  1100  0000  010
    0xf602 : "RMR_EL3",           # 11  110  1100  0000  010
    0xc681 : "CONTEXTIDR_EL1",    # 11  000  1101  0000  001
    0xde82 : "TPIDR_EL0",         # 11  011  1101  0000  010
    0xe682 : "TPIDR_EL2",         # 11  100  1101  0000  010
    0xf682 : "TPIDR_EL3",         # 11  110  1101  0000  010
    0xde83 : "TPIDRRO_EL0",       # 11  011  1101  0000  011
    0xc684 : "TPIDR_EL1",         # 11  000  1101  0000  100
    0xdf00 : "CNTFRQ_EL0",        # 11  011  1110  0000  000
    0xe703 : "CNTVOFF_EL2",       # 11  100  1110  0000  011
    0xc708 : "CNTKCTL_EL1",       # 11  000  1110  0001  000
    0xe708 : "CNTHCTL_EL2",       # 11  100  1110  0001  000
    0xdf10 : "CNTP_TVAL_EL0",     # 11  011  1110  0010  000
    0xe710 : "CNTHP_TVAL_EL2",    # 11  100  1110  0010  000
    0xff10 : "CNTPS_TVAL_EL1",    # 11  111  1110  0010  000
    0xdf11 : "CNTP_CTL_EL0",      # 11  011  1110  0010  001
    0xe711 : "CNTHP_CTL_EL2",     # 11  100  1110  0010  001
    0xff11 : "CNTPS_CTL_EL1",     # 11  111  1110  0010  001
    0xdf12 : "CNTP_CVAL_EL0",     # 11  011  1110  0010  010
    0xe712 : "CNTHP_CVAL_EL2",    # 11  100  1110  0010  010
    0xff12 : "CNTPS_CVAL_EL1",    # 11  111  1110  0010  010
    0xdf18 : "CNTV_TVAL_EL0",     # 11  011  1110  0011  000
    0xdf19 : "CNTV_CTL_EL0",      # 11  011  1110  0011  001
    0xdf1a : "CNTV_CVAL_EL0",     # 11  011  1110  0011  010
    0xdf40 : "PMEVCNTR0_EL0",     # 11  011  1110  1000  000
    0xdf41 : "PMEVCNTR1_EL0",     # 11  011  1110  1000  001
    0xdf42 : "PMEVCNTR2_EL0",     # 11  011  1110  1000  010
    0xdf43 : "PMEVCNTR3_EL0",     # 11  011  1110  1000  011
    0xdf44 : "PMEVCNTR4_EL0",     # 11  011  1110  1000  100
    0xdf45 : "PMEVCNTR5_EL0",     # 11  011  1110  1000  101
    0xdf46 : "PMEVCNTR6_EL0",     # 11  011  1110  1000  110
    0xdf47 : "PMEVCNTR7_EL0",     # 11  011  1110  1000  111
    0xdf48 : "PMEVCNTR8_EL0",     # 11  011  1110  1001  000
    0xdf49 : "PMEVCNTR9_EL0",     # 11  011  1110  1001  001
    0xdf4a : "PMEVCNTR10_EL0",    # 11  011  1110  1001  010
    0xdf4b : "PMEVCNTR11_EL0",    # 11  011  1110  1001  011
    0xdf4c : "PMEVCNTR12_EL0",    # 11  011  1110  1001  100
    0xdf4d : "PMEVCNTR13_EL0",    # 11  011  1110  1001  101
    0xdf4e : "PMEVCNTR14_EL0",    # 11  011  1110  1001  110
    0xdf4f : "PMEVCNTR15_EL0",    # 11  011  1110  1001  111
    0xdf50 : "PMEVCNTR16_EL0",    # 11  011  1110  1010  000
    0xdf51 : "PMEVCNTR17_EL0",    # 11  011  1110  1010  001
    0xdf52 : "PMEVCNTR18_EL0",    # 11  011  1110  1010  010
    0xdf53 : "PMEVCNTR19_EL0",    # 11  011  1110  1010  011
    0xdf54 : "PMEVCNTR20_EL0",    # 11  011  1110  1010  100
    0xdf55 : "PMEVCNTR21_EL0",    # 11  011  1110  1010  101
    0xdf56 : "PMEVCNTR22_EL0",    # 11  011  1110  1010  110
    0xdf57 : "PMEVCNTR23_EL0",    # 11  011  1110  1010  111
    0xdf58 : "PMEVCNTR24_EL0",    # 11  011  1110  1011  000
    0xdf59 : "PMEVCNTR25_EL0",    # 11  011  1110  1011  001
    0xdf5a : "PMEVCNTR26_EL0",    # 11  011  1110  1011  010
    0xdf5b : "PMEVCNTR27_EL0",    # 11  011  1110  1011  011
    0xdf5c : "PMEVCNTR28_EL0",    # 11  011  1110  1011  100
    0xdf5d : "PMEVCNTR29_EL0",    # 11  011  1110  1011  101
    0xdf5e : "PMEVCNTR30_EL0",    # 11  011  1110  1011  110
    0xdf7f : "PMCCFILTR_EL0",     # 11  011  1110  1111  111
    0xdf60 : "PMEVTYPER0_EL0",    # 11  011  1110  1100  000
    0xdf61 : "PMEVTYPER1_EL0",    # 11  011  1110  1100  001
    0xdf62 : "PMEVTYPER2_EL0",    # 11  011  1110  1100  010
    0xdf63 : "PMEVTYPER3_EL0",    # 11  011  1110  1100  011
    0xdf64 : "PMEVTYPER4_EL0",    # 11  011  1110  1100  100
    0xdf65 : "PMEVTYPER5_EL0",    # 11  011  1110  1100  101
    0xdf66 : "PMEVTYPER6_EL0",    # 11  011  1110  1100  110
    0xdf67 : "PMEVTYPER7_EL0",    # 11  011  1110  1100  111
    0xdf68 : "PMEVTYPER8_EL0",    # 11  011  1110  1101  000
    0xdf69 : "PMEVTYPER9_EL0",    # 11  011  1110  1101  001
    0xdf6a : "PMEVTYPER10_EL0",   # 11  011  1110  1101  010
    0xdf6b : "PMEVTYPER11_EL0",   # 11  011  1110  1101  011
    0xdf6c : "PMEVTYPER12_EL0",   # 11  011  1110  1101  100
    0xdf6d : "PMEVTYPER13_EL0",   # 11  011  1110  1101  101
    0xdf6e : "PMEVTYPER14_EL0",   # 11  011  1110  1101  110
    0xdf6f : "PMEVTYPER15_EL0",   # 11  011  1110  1101  111
    0xdf70 : "PMEVTYPER16_EL0",   # 11  011  1110  1110  000
    0xdf71 : "PMEVTYPER17_EL0",   # 11  011  1110  1110  001
    0xdf72 : "PMEVTYPER18_EL0",   # 11  011  1110  1110  010
    0xdf73 : "PMEVTYPER19_EL0",   # 11  011  1110  1110  011
    0xdf74 : "PMEVTYPER20_EL0",   # 11  011  1110  1110  100
    0xdf75 : "PMEVTYPER21_EL0",   # 11  011  1110  1110  101
    0xdf76 : "PMEVTYPER22_EL0",   # 11  011  1110  1110  110
    0xdf77 : "PMEVTYPER23_EL0",   # 11  011  1110  1110  111
    0xdf78 : "PMEVTYPER24_EL0",   # 11  011  1110  1111  000
    0xdf79 : "PMEVTYPER25_EL0",   # 11  011  1110  1111  001
    0xdf7a : "PMEVTYPER26_EL0",   # 11  011  1110  1111  010
    0xdf7b : "PMEVTYPER27_EL0",   # 11  011  1110  1111  011
    0xdf7c : "PMEVTYPER28_EL0",   # 11  011  1110  1111  100
    0xdf7d : "PMEVTYPER29_EL0",   # 11  011  1110  1111  101
    0xdf7e : "PMEVTYPER30_EL0",   # 11  011  1110  1111  110
    0x8808 : "TRCPRGCTLR",        # 10  001  0000  0001  000
    0x8810 : "TRCPROCSELR",       # 10  001  0000  0010  000
    0x8820 : "TRCCONFIGR",        # 10  001  0000  0100  000
    0x8830 : "TRCAUXCTLR",        # 10  001  0000  0110  000
    0x8840 : "TRCEVENTCTL0R",     # 10  001  0000  1000  000
    0x8848 : "TRCEVENTCTL1R",     # 10  001  0000  1001  000
    0x8858 : "TRCSTALLCTLR",      # 10  001  0000  1011  000
    0x8860 : "TRCTSCTLR",         # 10  001  0000  1100  000
    0x8868 : "TRCSYNCPR",         # 10  001  0000  1101  000
    0x8870 : "TRCCCCTLR",         # 10  001  0000  1110  000
    0x8878 : "TRCBBCTLR",         # 10  001  0000  1111  000
    0x8801 : "TRCTRACEIDR",       # 10  001  0000  0000  001
    0x8809 : "TRCQCTLR",          # 10  001  0000  0001  001
    0x8802 : "TRCVICTLR",         # 10  001  0000  0000  010
    0x880a : "TRCVIIECTLR",       # 10  001  0000  0001  010
    0x8812 : "TRCVISSCTLR",       # 10  001  0000  0010  010
    0x881a : "TRCVIPCSSCTLR",     # 10  001  0000  0011  010
    0x8842 : "TRCVDCTLR",         # 10  001  0000  1000  010
    0x884a : "TRCVDSACCTLR",      # 10  001  0000  1001  010
    0x8852 : "TRCVDARCCTLR",      # 10  001  0000  1010  010
    0x8804 : "TRCSEQEVR0",        # 10  001  0000  0000  100
    0x880c : "TRCSEQEVR1",        # 10  001  0000  0001  100
    0x8814 : "TRCSEQEVR2",        # 10  001  0000  0010  100
    0x8834 : "TRCSEQRSTEVR",      # 10  001  0000  0110  100
    0x883c : "TRCSEQSTR",         # 10  001  0000  0111  100
    0x8844 : "TRCEXTINSELR",      # 10  001  0000  1000  100
    0x8805 : "TRCCNTRLDVR0",      # 10  001  0000  0000  101
    0x880d : "TRCCNTRLDVR1",      # 10  001  0000  0001  101
    0x8815 : "TRCCNTRLDVR2",      # 10  001  0000  0010  101
    0x881d : "TRCCNTRLDVR3",      # 10  001  0000  0011  101
    0x8825 : "TRCCNTCTLR0",       # 10  001  0000  0100  101
    0x882d : "TRCCNTCTLR1",       # 10  001  0000  0101  101
    0x8835 : "TRCCNTCTLR2",       # 10  001  0000  0110  101
    0x883d : "TRCCNTCTLR3",       # 10  001  0000  0111  101
    0x8845 : "TRCCNTVR0",         # 10  001  0000  1000  101
    0x884d : "TRCCNTVR1",         # 10  001  0000  1001  101
    0x8855 : "TRCCNTVR2",         # 10  001  0000  1010  101
    0x885d : "TRCCNTVR3",         # 10  001  0000  1011  101
    0x8807 : "TRCIMSPEC0",        # 10  001  0000  0000  111
    0x880f : "TRCIMSPEC1",        # 10  001  0000  0001  111
    0x8817 : "TRCIMSPEC2",        # 10  001  0000  0010  111
    0x881f : "TRCIMSPEC3",        # 10  001  0000  0011  111
    0x8827 : "TRCIMSPEC4",        # 10  001  0000  0100  111
    0x882f : "TRCIMSPEC5",        # 10  001  0000  0101  111
    0x8837 : "TRCIMSPEC6",        # 10  001  0000  0110  111
    0x883f : "TRCIMSPEC7",        # 10  001  0000  0111  111
    0x8890 : "TRCRSCTLR2",        # 10  001  0001  0010  000
    0x8898 : "TRCRSCTLR3",        # 10  001  0001  0011  000
    0x88a0 : "TRCRSCTLR4",        # 10  001  0001  0100  000
    0x88a8 : "TRCRSCTLR5",        # 10  001  0001  0101  000
    0x88b0 : "TRCRSCTLR6",        # 10  001  0001  0110  000
    0x88b8 : "TRCRSCTLR7",        # 10  001  0001  0111  000
    0x88c0 : "TRCRSCTLR8",        # 10  001  0001  1000  000
    0x88c8 : "TRCRSCTLR9",        # 10  001  0001  1001  000
    0x88d0 : "TRCRSCTLR10",       # 10  001  0001  1010  000
    0x88d8 : "TRCRSCTLR11",       # 10  001  0001  1011  000
    0x88e0 : "TRCRSCTLR12",       # 10  001  0001  1100  000
    0x88e8 : "TRCRSCTLR13",       # 10  001  0001  1101  000
    0x88f0 : "TRCRSCTLR14",       # 10  001  0001  1110  000
    0x88f8 : "TRCRSCTLR15",       # 10  001  0001  1111  000
    0x8881 : "TRCRSCTLR16",       # 10  001  0001  0000  001
    0x8889 : "TRCRSCTLR17",       # 10  001  0001  0001  001
    0x8891 : "TRCRSCTLR18",       # 10  001  0001  0010  001
    0x8899 : "TRCRSCTLR19",       # 10  001  0001  0011  001
    0x88a1 : "TRCRSCTLR20",       # 10  001  0001  0100  001
    0x88a9 : "TRCRSCTLR21",       # 10  001  0001  0101  001
    0x88b1 : "TRCRSCTLR22",       # 10  001  0001  0110  001
    0x88b9 : "TRCRSCTLR23",       # 10  001  0001  0111  001
    0x88c1 : "TRCRSCTLR24",       # 10  001  0001  1000  001
    0x88c9 : "TRCRSCTLR25",       # 10  001  0001  1001  001
    0x88d1 : "TRCRSCTLR26",       # 10  001  0001  1010  001
    0x88d9 : "TRCRSCTLR27",       # 10  001  0001  1011  001
    0x88e1 : "TRCRSCTLR28",       # 10  001  0001  1100  001
    0x88e9 : "TRCRSCTLR29",       # 10  001  0001  1101  001
    0x88f1 : "TRCRSCTLR30",       # 10  001  0001  1110  001
    0x88f9 : "TRCRSCTLR31",       # 10  001  0001  1111  001
    0x8882 : "TRCSSCCR0",         # 10  001  0001  0000  010
    0x888a : "TRCSSCCR1",         # 10  001  0001  0001  010
    0x8892 : "TRCSSCCR2",         # 10  001  0001  0010  010
    0x889a : "TRCSSCCR3",         # 10  001  0001  0011  010
    0x88a2 : "TRCSSCCR4",         # 10  001  0001  0100  010
    0x88aa : "TRCSSCCR5",         # 10  001  0001  0101  010
    0x88b2 : "TRCSSCCR6",         # 10  001  0001  0110  010
    0x88ba : "TRCSSCCR7",         # 10  001  0001  0111  010
    0x88c2 : "TRCSSCSR0",         # 10  001  0001  1000  010
    0x88ca : "TRCSSCSR1",         # 10  001  0001  1001  010
    0x88d2 : "TRCSSCSR2",         # 10  001  0001  1010  010
    0x88da : "TRCSSCSR3",         # 10  001  0001  1011  010
    0x88e2 : "TRCSSCSR4",         # 10  001  0001  1100  010
    0x88ea : "TRCSSCSR5",         # 10  001  0001  1101  010
    0x88f2 : "TRCSSCSR6",         # 10  001  0001  1110  010
    0x88fa : "TRCSSCSR7",         # 10  001  0001  1111  010
    0x8883 : "TRCSSPCICR0",       # 10  001  0001  0000  011
    0x888b : "TRCSSPCICR1",       # 10  001  0001  0001  011
    0x8893 : "TRCSSPCICR2",       # 10  001  0001  0010  011
    0x889b : "TRCSSPCICR3",       # 10  001  0001  0011  011
    0x88a3 : "TRCSSPCICR4",       # 10  001  0001  0100  011
    0x88ab : "TRCSSPCICR5",       # 10  001  0001  0101  011
    0x88b3 : "TRCSSPCICR6",       # 10  001  0001  0110  011
    0x88bb : "TRCSSPCICR7",       # 10  001  0001  0111  011
    0x88a4 : "TRCPDCR",           # 10  001  0001  0100  100
    0x8900 : "TRCACVR0",          # 10  001  0010  0000  000
    0x8910 : "TRCACVR1",          # 10  001  0010  0010  000
    0x8920 : "TRCACVR2",          # 10  001  0010  0100  000
    0x8930 : "TRCACVR3",          # 10  001  0010  0110  000
    0x8940 : "TRCACVR4",          # 10  001  0010  1000  000
    0x8950 : "TRCACVR5",          # 10  001  0010  1010  000
    0x8960 : "TRCACVR6",          # 10  001  0010  1100  000
    0x8970 : "TRCACVR7",          # 10  001  0010  1110  000
    0x8901 : "TRCACVR8",          # 10  001  0010  0000  001
    0x8911 : "TRCACVR9",          # 10  001  0010  0010  001
    0x8921 : "TRCACVR10",         # 10  001  0010  0100  001
    0x8931 : "TRCACVR11",         # 10  001  0010  0110  001
    0x8941 : "TRCACVR12",         # 10  001  0010  1000  001
    0x8951 : "TRCACVR13",         # 10  001  0010  1010  001
    0x8961 : "TRCACVR14",         # 10  001  0010  1100  001
    0x8971 : "TRCACVR15",         # 10  001  0010  1110  001
    0x8902 : "TRCACATR0",         # 10  001  0010  0000  010
    0x8912 : "TRCACATR1",         # 10  001  0010  0010  010
    0x8922 : "TRCACATR2",         # 10  001  0010  0100  010
    0x8932 : "TRCACATR3",         # 10  001  0010  0110  010
    0x8942 : "TRCACATR4",         # 10  001  0010  1000  010
    0x8952 : "TRCACATR5",         # 10  001  0010  1010  010
    0x8962 : "TRCACATR6",         # 10  001  0010  1100  010
    0x8972 : "TRCACATR7",         # 10  001  0010  1110  010
    0x8903 : "TRCACATR8",         # 10  001  0010  0000  011
    0x8913 : "TRCACATR9",         # 10  001  0010  0010  011
    0x8923 : "TRCACATR10",        # 10  001  0010  0100  011
    0x8933 : "TRCACATR11",        # 10  001  0010  0110  011
    0x8943 : "TRCACATR12",        # 10  001  0010  1000  011
    0x8953 : "TRCACATR13",        # 10  001  0010  1010  011
    0x8963 : "TRCACATR14",        # 10  001  0010  1100  011
    0x8973 : "TRCACATR15",        # 10  001  0010  1110  011
    0x8904 : "TRCDVCVR0",         # 10  001  0010  0000  100
    0x8924 : "TRCDVCVR1",         # 10  001  0010  0100  100
    0x8944 : "TRCDVCVR2",         # 10  001  0010  1000  100
    0x8964 : "TRCDVCVR3",         # 10  001  0010  1100  100
    0x8905 : "TRCDVCVR4",         # 10  001  0010  0000  101
    0x8925 : "TRCDVCVR5",         # 10  001  0010  0100  101
    0x8945 : "TRCDVCVR6",         # 10  001  0010  1000  101
    0x8965 : "TRCDVCVR7",         # 10  001  0010  1100  101
    0x8906 : "TRCDVCMR0",         # 10  001  0010  0000  110
    0x8926 : "TRCDVCMR1",         # 10  001  0010  0100  110
    0x8946 : "TRCDVCMR2",         # 10  001  0010  1000  110
    0x8966 : "TRCDVCMR3",         # 10  001  0010  1100  110
    0x8907 : "TRCDVCMR4",         # 10  001  0010  0000  111
    0x8927 : "TRCDVCMR5",         # 10  001  0010  0100  111
    0x8947 : "TRCDVCMR6",         # 10  001  0010  1000  111
    0x8967 : "TRCDVCMR7",         # 10  001  0010  1100  111
    0x8980 : "TRCCIDCVR0",        # 10  001  0011  0000  000
    0x8990 : "TRCCIDCVR1",        # 10  001  0011  0010  000
    0x89a0 : "TRCCIDCVR2",        # 10  001  0011  0100  000
    0x89b0 : "TRCCIDCVR3",        # 10  001  0011  0110  000
    0x89c0 : "TRCCIDCVR4",        # 10  001  0011  1000  000
    0x89d0 : "TRCCIDCVR5",        # 10  001  0011  1010  000
    0x89e0 : "TRCCIDCVR6",        # 10  001  0011  1100  000
    0x89f0 : "TRCCIDCVR7",        # 10  001  0011  1110  000
    0x8981 : "TRCVMIDCVR0",       # 10  001  0011  0000  001
    0x8991 : "TRCVMIDCVR1",       # 10  001  0011  0010  001
    0x89a1 : "TRCVMIDCVR2",       # 10  001  0011  0100  001
    0x89b1 : "TRCVMIDCVR3",       # 10  001  0011  0110  001
    0x89c1 : "TRCVMIDCVR4",       # 10  001  0011  1000  001
    0x89d1 : "TRCVMIDCVR5",       # 10  001  0011  1010  001
    0x89e1 : "TRCVMIDCVR6",       # 10  001  0011  1100  001
    0x89f1 : "TRCVMIDCVR7",       # 10  001  0011  1110  001
    0x8982 : "TRCCIDCCTLR0",      # 10  001  0011  0000  010
    0x898a : "TRCCIDCCTLR1",      # 10  001  0011  0001  010
    0x8992 : "TRCVMIDCCTLR0",     # 10  001  0011  0010  010
    0x899a : "TRCVMIDCCTLR1",     # 10  001  0011  0011  010
    0x8b84 : "TRCITCTRL",         # 10  001  0111  0000  100
    0x8bc6 : "TRCCLAIMSET",       # 10  001  0111  1000  110
    0x8bce : "TRCCLAIMCLR",       # 10  001  0111  1001  110
    0xc663 : "ICC_BPR1_EL1",      # 11  000  1100  1100  011
    0xc643 : "ICC_BPR0_EL1",      # 11  000  1100  1000  011
    0xc230 : "ICC_PMR_EL1",       # 11  000  0100  0110  000
    0xc664 : "ICC_CTLR_EL1",      # 11  000  1100  1100  100
    0xf664 : "ICC_CTLR_EL3",      # 11  110  1100  1100  100
    0xc665 : "ICC_SRE_EL1",       # 11  000  1100  1100  101
    0xe64d : "ICC_SRE_EL2",       # 11  100  1100  1001  101
    0xf665 : "ICC_SRE_EL3",       # 11  110  1100  1100  101
    0xc666 : "ICC_IGRPEN0_EL1",   # 11  000  1100  1100  110
    0xc667 : "ICC_IGRPEN1_EL1",   # 11  000  1100  1100  111
    0xf667 : "ICC_IGRPEN1_EL3",   # 11  110  1100  1100  111
    0xc668 : "ICC_SEIEN_EL1",     # 11  000  1100  1101  000
    0xc644 : "ICC_AP0R0_EL1",     # 11  000  1100  1000  100
    0xc645 : "ICC_AP0R1_EL1",     # 11  000  1100  1000  101
    0xc646 : "ICC_AP0R2_EL1",     # 11  000  1100  1000  110
    0xc647 : "ICC_AP0R3_EL1",     # 11  000  1100  1000  111
    0xc648 : "ICC_AP1R0_EL1",     # 11  000  1100  1001  000
    0xc649 : "ICC_AP1R1_EL1",     # 11  000  1100  1001  001
    0xc64a : "ICC_AP1R2_EL1",     # 11  000  1100  1001  010
    0xc64b : "ICC_AP1R3_EL1",     # 11  000  1100  1001  011
    0xe640 : "ICH_AP0R0_EL2",     # 11  100  1100  1000  000
    0xe641 : "ICH_AP0R1_EL2",     # 11  100  1100  1000  001
    0xe642 : "ICH_AP0R2_EL2",     # 11  100  1100  1000  010
    0xe643 : "ICH_AP0R3_EL2",     # 11  100  1100  1000  011
    0xe648 : "ICH_AP1R0_EL2",     # 11  100  1100  1001  000
    0xe649 : "ICH_AP1R1_EL2",     # 11  100  1100  1001  001
    0xe64a : "ICH_AP1R2_EL2",     # 11  100  1100  1001  010
    0xe64b : "ICH_AP1R3_EL2",     # 11  100  1100  1001  011
    0xe658 : "ICH_HCR_EL2",       # 11  100  1100  1011  000
    0xe65a : "ICH_MISR_EL2",      # 11  100  1100  1011  010
    0xe65f : "ICH_VMCR_EL2",      # 11  100  1100  1011  111
    0xe64c : "ICH_VSEIR_EL2",     # 11  100  1100  1001  100
    0xe660 : "ICH_LR0_EL2",       # 11  100  1100  1100  000
    0xe661 : "ICH_LR1_EL2",       # 11  100  1100  1100  001
    0xe662 : "ICH_LR2_EL2",       # 11  100  1100  1100  010
    0xe663 : "ICH_LR3_EL2",       # 11  100  1100  1100  011
    0xe664 : "ICH_LR4_EL2",       # 11  100  1100  1100  100
    0xe665 : "ICH_LR5_EL2",       # 11  100  1100  1100  101
    0xe666 : "ICH_LR6_EL2",       # 11  100  1100  1100  110
    0xe667 : "ICH_LR7_EL2",       # 11  100  1100  1100  111
    0xe668 : "ICH_LR8_EL2",       # 11  100  1100  1101  000
    0xe669 : "ICH_LR9_EL2",       # 11  100  1100  1101  001
    0xe66a : "ICH_LR10_EL2",      # 11  100  1100  1101  010
    0xe66b : "ICH_LR11_EL2",      # 11  100  1100  1101  011
    0xe66c : "ICH_LR12_EL2",      # 11  100  1100  1101  100
    0xe66d : "ICH_LR13_EL2",      # 11  100  1100  1101  101
    0xe66e : "ICH_LR14_EL2",      # 11  100  1100  1101  110
    0xe66f : "ICH_LR15_EL2",      # 11  100  1100  1101  111
    0xff90 : "CPM_IOACC_CTL_EL3"
}
shifts = [ 14, 11, 7, 3, 0 ]

inttype = None
myenum = "ARM64_SYSREG_aenum"

class cblock_visitor_t(idaapi.ctree_visitor_t):
    def __init__(self):
        idaapi.ctree_visitor_t.__init__(self, idaapi.CV_FAST)
        return

    def visit_expr(self, expr):
        try:
            if expr.op == idaapi.cot_call and expr.x.op == idaapi.cot_helper:
                #print idaapi.tag_remove(expr.x.print1(None))
                if expr.x.helper == "ARM64_SYSREG" and len(expr.a) == 5:
                    reg = 0
                    for j, i in enumerate(expr.a):
                        if i.type != inttype:
                            break
                        #print i.n.value(i.type)
                        reg = reg | (i.numval() << shifts[j])
                    else:
                        if reg in regs.keys():
                            # apparently, we cannot change the name
                            # so remove all params but the first one,
                            # make it symbolic, and set its value accordingly
                            while len(expr.a) > 1:
                                expr.a.pop_back()
                            expr.a[0].n.nf.flags = idaapi.enumflag()
                            expr.a[0].n.nf.serial = 0
                            expr.a[0].n.nf.type_name = myenum
                            expr.a[0].n._value = reg
                            #print "ok"
        except:
            traceback.print_exc()
        return 0

class hexrays_callback_info(object):
    def __init__(self):
        return

    def event_callback(self, event, *args):
        try:
            if event == idaapi.hxe_maturity:
                cfunc, maturity = args
                if maturity == idaapi.CMAT_BUILT:
                    cbv = cblock_visitor_t()
                    cbv.apply_to(cfunc.body, None)
        except:
            traceback.print_exc()
        return 0

def remove():
    if hexnight_cb:
        idaapi.remove_hexrays_callback(hexnight_cb)

class HexHNightPlugin_t(idaapi.plugin_t):
    flags = idaapi.PLUGIN_HIDE
    comment = "show symbolic names for ARM64_SYSREG in Pseudocode-View"
    help = "Runs transparently"
    wanted_name = "HexNight"
    wanted_hotkey = ""

    def init(self):
        # Some initialization
        global hexnight_cb_info, hexnight_cb, inttype

        if idaapi.init_hexrays_plugin() and idaapi.ph_get_id() == idaapi.PLFM_ARM and idaapi.BADADDR > 0xFFFFFFFF:
            inttype = idaapi.get_int_type_by_width_and_sign(4, True)
            enu = idaapi.add_enum(0, myenum, 0)
            for i in regs.keys():
                idaapi.add_enum_member(enu, regs[i], i)
            hexnight_cb_info = hexrays_callback_info()
            hexnight_cb = hexnight_cb_info.event_callback
            if idaapi.install_hexrays_callback(hexnight_cb):
                print "Hexnight plugin installed"
                addon = idaapi.addon_info_t();
                addon.id = "org.xerub.hexnight";
                addon.name = "Hexnight";
                addon.producer = "xerub";
                addon.url = "https://twitter.com/xerub";
                addon.version = "6.95";
                idaapi.register_addon( addon );
                return idaapi.PLUGIN_KEEP
        print "Hexnight plugin failed"
        return idaapi.PLUGIN_SKIP

    def run(self, arg=0):
        return

    def term(self):
        remove()

def PLUGIN_ENTRY():
    return HexHNightPlugin_t()
