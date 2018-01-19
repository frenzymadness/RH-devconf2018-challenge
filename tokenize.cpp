/* tokenize.cpp
 *
 * Copyright (C) 2018 Red Hat, Inc.
 *
 * Authors: Jiri Vymazal <jvymazal@redhat.com>
 *
 */

#include <iostream>

#include <clang-c/Index.h>

int Tokenize(const std::string& filepath) 
{
	const int exclude_decls_from_pch = 1;
	const int display_diagnostics = 0;
	CXIndex index = clang_createIndex(exclude_decls_from_pch, display_diagnostics);
	const unsigned index_options = CXGlobalOpt_None;
	clang_CXIndex_setGlobalOptions(index, index_options);
	const char* command_line_args[] = { "-Xclang", "-cc1" };
	const int num_command_line_args = sizeof(command_line_args) / sizeof(char*);
	const unsigned num_unsaved_files = 0;
	CXUnsavedFile* unsaved_files = NULL;
	CXTranslationUnit tu = clang_createTranslationUnitFromSourceFile(index, filepath.c_str(), num_command_line_args, command_line_args, num_unsaved_files, unsaved_files);
	if (tu != NULL) 
	{
 		CXCursor cursor = clang_getTranslationUnitCursor(tu);
	 	CXSourceRange range = clang_getCursorExtent(cursor);
 		CXToken* tokens = NULL;
		unsigned num_tokens = 0;
	 	clang_tokenize(tu, range, &tokens, &num_tokens);
		std::cout << num_tokens << std::endl;
 		clang_disposeTranslationUnit(tu);
	} 
	else 
	{
		std::cerr << "Failed to tokenize: \"" << filepath << "\"" << std::endl;
		return EXIT_FAILURE;
	}
	clang_disposeIndex(index);
	return EXIT_SUCCESS;
}

int main(int argc, char** argv) 
{
	if (argc < 2) 
	{
		return EXIT_FAILURE;
	}
	std::string filepath(argv[1]);
	return Tokenize(filepath);
}
