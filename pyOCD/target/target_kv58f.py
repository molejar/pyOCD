"""
 mbed CMSIS-DAP debugger
 Copyright (c) 2006-2013 ARM Limited

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

from target_kinetis import Kinetis
from .memory_map import (FlashRegion, RamRegion, MemoryMap)
import logging
from cortex_m import (NVIC_AIRCR, NVIC_AIRCR_SYSRESETREQ)
from ..transport.transport import TransferError

class KV58F(Kinetis):

    singleMap = MemoryMap(
        FlashRegion(name='flash', start=0x10000000, length=0x100000, blocksize=0x2000, isBootMemory=True),
        RamRegion(name='ram0', start=0x00000000, length=0x10000),
        RamRegion(name='ram1', start=0x18000000, length=0x1000),
        RamRegion(name='ram2', start=0x20000000, length=0x20000),
        RamRegion(name='ram3', start=0x2F000000, length=0x10000)
        )

    def __init__(self, transport):
        super(KV58F, self).__init__(transport, self.singleMap)
        self.mdm_idr = 0x001c0030
        self.is_dual_core = False

    def reset(self, software_reset = None):
        try:
            super(KV58F, self).reset(software_reset)
        except TransferError:
            # KL28 causes a SWD transfer fault for the AIRCR write when
            # it resets. Just ignore this error.
            pass

