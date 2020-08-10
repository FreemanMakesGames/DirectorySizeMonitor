# Directory Size Monitor
Directory Size Monitor is a tool that can show the user what are some biggest files and directories on the file system, as well as some biggest size changes of files and directories over a period of time.

# Installation
Simply download the release.
Currently there is only Windows version. It may be a good idea to put it into `C:\Program Files\DirectorySizeMonitor`, and create a desktop shortcut to `DirectorySizeMonitor.exe`.

# Usage
Typical use of this tool starts with these steps:
1. Click the "Scan" button at the top-left.
2. Select the "target directory" you want to scan.
3. Sort by size.

Now you will be shown the files and directories under your target directory, sorted from big to small.

This was the original motivation for the project. In Windows's file explorer, directory sizes are hidden. It's really hard to get an overview, or to find out which directory or file takes up the most space. Directory Size Monitor helps with this problem.

## Scan Depth
You can enter the depth for a scan. With each added depth, the directories will be further opened up, and have their contents scanned.

Currently only a depth between 1 to 5 is supported.

## Display Depth
You can display by hierarchy, which resembles how the file system is usually displayed by OS. Or you can display by depth. Various depths give various granularities. For a hypothetical example, if you scan the C drive with a depth of 5, but display the result with a depth of 1, it'll show that `C:/dir1` is the biggest entry. But if you display with a depth of 2, `C:/dir1` and other directories will be broken up. Maybe now `C:/dir5/file1` is the biggest entry, and nothing from `C:/dir1` ranks high, because `C:/dir1` consists of a lot of small files.

## Monitoring size changes over time
Directory Size Monitor's second feature is examining size changes of files and directories under the target directory you selected. Before you start, remember that comparison can only be made between scans under the same target directory, with a same depth. Now, to use this feature:
1. Scan a target directory with a desired depth.
2. Click "Save Result", which will prompt you to save into a JSON file.
3. After a period of time, scan the same target directory again, with the same depth.
4. Click "Load and Compare", and load the file you saved last time.
The tool will then show you the changes in size of files and directories since last time, as well as new and deleted entries.

# Errors
Errors will be reported in the view at the bottom. Currently on Windows, there are 2 known errors.
1. `WinError 5` This can be solved if you run the program as administrator.
2. `WinError 1920` Some of these may be solved by running the program as administrator. But a lot cannot. These are probably files or directories that can be accessed only by the "system".
