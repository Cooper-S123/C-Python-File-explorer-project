#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>

//function to show files/subfolders in current directory
void list_current_dir(const char *path, void (*python_append_callback)(const char *)) {
  struct dirent *current;
  DIR *dir = opendir(path);

  //error check
  if (dir == NULL) {
    perror("directory didn't open");
    return;
  }
  
  while ((current = readdir(dir)) != NULL) {
    //remove the local files
    if (strcmp(current->d_name, ".") == 0 || strcmp(current->d_name, "..") == 0) {
        continue;
    }
    //add the current file to the python list
    python_append_callback(current->d_name);
  }

}