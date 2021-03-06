// Code wrapping the AXI4 (FPGA) and
// file (XDMA driver) abstractions to a common 'DMA message'

#pragma once
#include "../../uintN_t.h"

// Current DMA example requires:
// 	Minimum 64 bytes messages (1 cycle of aligned AXI4 512b data)
//    Maximum tested was 4096
//    Only tested sizes multiple of 64 bytes 
#define DMA_MSG_SIZE 4096
#define dma_msg_size_t uint16_t
typedef struct dma_msg_t
{
  uint8_t data[DMA_MSG_SIZE];
} dma_msg_t;
dma_msg_t DMA_MSG_T_NULL()
{
  dma_msg_t rv;
  dma_msg_size_t i;
  for(i=0;i<DMA_MSG_SIZE;i=i+1)
  {
    rv.data[i] = 0;
  }
  return rv;
}

// Stream version of message with valid flag
typedef struct dma_msg_s
{
  dma_msg_t data; // The message
  uint1_t valid;
} dma_msg_s;
dma_msg_s DMA_MSG_S_NULL()
{
  dma_msg_s rv;
  rv.data = DMA_MSG_T_NULL();
  rv.valid = 0;
  return rv;
}
