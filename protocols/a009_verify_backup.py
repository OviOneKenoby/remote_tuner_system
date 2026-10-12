"""Offline private backup preflight only. No serial, write, erase or upload API."""
import argparse,hashlib,json,struct
from pathlib import Path
BASELINE_TABLE_SHA='d7ffd497cfcd33e697304b3cf8112e7a1f1cb0619639fe9879ed431cbbdc8835'
BASELINE_SECTOR_SHA='4946a42576c9e499c4a856b9104abfb6d09fff4f3fff2cd7985649ccbcec8f46'
BASELINE_IMAGE_SHA='7e8d77c21898014fbd7ea625cf2d25aa7f77941d5ba1d24484090f7361279afb'
def digest(b):return hashlib.sha256(b).hexdigest()
def inspect(backup,output):
 data=Path(backup).read_bytes()
 if len(data)!=0x1000000:raise ValueError('STOP: backup must contain exactly16MiB')
 sector=data[0x8000:0x9000]
 if digest(sector)!=BASELINE_SECTOR_SHA or digest(sector[:3072])!=BASELINE_TABLE_SHA:
  raise ValueError('STOP: current partition table differs from accepted baseline')
 if any(b!=255 for b in data[0xE20000:0xE30000]):
  raise ValueError('STOP: proposed region is not completely erased; do not erase it')
 if any(b!=255 for b in data[0x810000:0x812000]):
  raise ValueError('STOP: OTA metadata differs; running-image selection needs review')
 image=data[0x10000:0x810000]
 if image[0]!=0xE9 or image[1]>16:raise ValueError('STOP: invalid factory image header')
 cursor=24;checksum=0xEF;descriptor=None
 for _ in range(image[1]):
  if cursor+8>len(image):raise ValueError('STOP: truncated image segment header')
  address,size=struct.unpack_from('<II',image,cursor);cursor+=8
  if cursor+size>len(image):raise ValueError('STOP: image exceeds factory bounds')
  body=image[cursor:cursor+size]
  for b in body:checksum^=b
  if descriptor is None and len(body)>=256 and body[:4]==struct.pack('<I',0xABCD5432):
   def field(a,z):return body[a:z].split(b'\0',1)[0].decode('utf8','replace')
   descriptor={'project':field(48,80),'version':field(16,48),'time':field(80,96),'date':field(96,112),'IDF':field(112,144),'ELF_sha256':body[144:176].hex()}
  cursor+=size
 checksum_offset=(cursor+16)//16*16-1
 if checksum_offset>=len(image) or image[checksum_offset]!=checksum:raise ValueError('STOP: factory checksum invalid')
 end=checksum_offset+1
 if image[23]==1:
  if digest(image[:end])!=image[end:end+32].hex():raise ValueError('STOP: appended factory digest invalid')
  end+=32
 firmware_sha=digest(image[:end])
 if firmware_sha!=BASELINE_IMAGE_SHA:raise ValueError('STOP: current factory image differs from accepted A007 identity')
 result={'status':'PASS','backup_bytes':len(data),'backup_sha256':digest(data),'partition_sector_sha256':digest(sector),'partition_binary_sha256':digest(sector[:3072]),'candidate_region_erased_bytes':65536,'otadata':'all FF; factory default selection','factory_offset':'0x10000','factory_image_bytes':end,'factory_image_sha256':firmware_sha,'factory_descriptor':descriptor,'runtime_identity':'Image bytes verified; running behavior requires owner observation','hardware_operations':'NONE; this helper reads only a local backup','privacy':'Keep full backup and output local; no raw flash/NVS contents published'}
 Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
 return result
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--backup',required=True);parser.add_argument('--output',required=True)
 args=parser.parse_args()
 try:
  result=inspect(args.backup,args.output)
  print('PASS: complete backup, accepted partition table/factory image and erased target region verified offline.')
 except (OSError,ValueError) as e:
  parser.exit(1,str(e)+'\n')
