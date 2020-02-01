// Code wrapping the AXI4 (FPGA) and
// file (XDMA driver) abstractions to a common 'DMA message'

#pragma once
#include "../../uintN_t.h"

// Current DMA example requires:
// 	Minimum 64 bytes messages (1 cycle of aligned AXI4 512b data)
//  Maximum 4096 bytes messages (1 AXI4 burst)
//	Size must be multiple of 64 bytes
#define DMA_MSG_SIZE 1024
#define LOG2_DMA_MSG_SIZE_DIV_FLOAT_SIZE_PLUS1 9 // log2(DMA_MSG_SIZE/4)+1
#define dma_msg_size_t uint16_t
typedef struct dma_msg_t
{
  uint8_t data[DMA_MSG_SIZE];
} dma_msg_t;
// Stream version for buffering
typedef struct dma_msg_s
{
  dma_msg_t data;
  uint1_t valid;
} dma_msg_s;