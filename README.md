# BashMate 🚀

Your Ultimate Companion for Bash Productivity!

![BashMate Logo](logo.png)

## Description

BashMate is a curated collection of bash commands, functions, and aliases designed to supercharge your terminal experience. Whether you're wrangling Git, managing macOS specifics, or sailing through Laravel tasks, BashMate is here to assist. Explore, contribute, and make your command-line experience efficient and enjoyable!

## Features

- **Git Enhancements**: Simplified git commands and useful aliases.
- **macOS Utilities**: Tools specifically tailored for macOS users.
- **Laravel Shortcuts**: Commands to streamline Laravel development.
- **Envoyer.io Api Commands**: Commands to consult deployment status of envoyer.io projects.
- **And More!**: Discover various other utilities to boost your productivity.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LounisBou/BashMate.git
   ```

2. Source the main bash file (or add this to your .bashrc or .zshrc for permanent use):
  ```bash
  cd BashMate
  echo "source $(PWD)/bashmate.sh" >> ~/.zshrc
  ```

## Documentation

### BashMate Aliases and Functions

**Note**: This section documents various aliases and functions for the bourne again shell. These were created by LounisBou.

#### General Shell Utilities

- **Restart bash**: 
  ```bash
  rebash
  ```

- **Restart zsh**:
  ```bash
  rezsh
  ```

- **Shutdown**:
  ```bash
  shutdown
  ```

- **Reboot**:
  ```bash
  reboot
  ```

- **List all files**: 
  ```bash
  ll
  ```

- **Get the real path of a file**: 
  ```bash
  path
  ```

- **Clear terminal**: 
  ```bash
  cl
  ```

- **Watch aliases**:
  ```bash
  watcha
  ```

#### System User Utilities

- **Add group to user**: 
  ```bash
  add-group
  ```

#### Filesystem Utilities

- **Create folder for each file**: 
  ```bash
  folderPack
  ```

- **Rename files**: 
  ```bash
  rname
  ```

#### Network Utilities (using NMAP)

- **Check all machines on LAN**: 
  ```bash
  onLan
  ```

- **Check for specific port on LAN**:
  ```bash
  onLanPort
  ```

#### Compression & Decompression (using TAR)

- **Compress folder in tar.gz file**: 
  ```bash
  targz
  ```

- **Uncompress tar.gz file**:
  ```bash
  untargz
  ```

### BrewMate: Homebrew Utilities for BashMate

This section documents various functions and aliases designed to manage Homebrew services and updates.

#### Brew Services Management

- **View and manage services**: 
  ```bash
  services
  ```

- **Start a service**: 
  ```bash
  start
  ```

- **Start a service with sudo**:
  ```bash
  sstart
  ```

- **Stop a service**: 
  ```bash
  stop
  ```

- **Stop a service with sudo**:
  ```bash
  sstop
  ```

- **Restart a service**:
  ```bash
  restart
  ```

- **Restart a service with sudo**:
  ```bash
  srestart
  ```

#### Brew Update Utilities

- **Update, upgrade, clean, and check Homebrew**: 
  ```bash
  brewup
  ```

- **Update, upgrade, clean, check Homebrew, and upgrade casks**:
  ```bash
  brewupc
  ```

### EnvoyerMate: Envoyer API Utilities for BashMate

This section documents various functions designed to interact with the Envoyer API. These utilities allow you to fetch and display project and deployment information.

---

#### List of All Projects: `envoyer-projects`

Displays a list of all the projects fetched from the Envoyer API.

Usage:
```bash
envoyer-projects
```

---

Ensure you include any required instructions or prerequisites for using these functions. For example, users might need to have `jq` and `curl` utilities installed and the API endpoint & token should be correctly set in the environment variables.

---

#### Specific Project Details:

Fetches and displays detailed information of a specific project from the Envoyer API based on the provided Project ID.

Usage:
```bash
envoyer-project [PROJECT_ID]
```

**Note**: Make sure the environment variables `$ENVOYER_API_URL` and `$ENVOYER_API_TOKEN` are set correctly before using these functions. Also, it's a good practice to have the `jq` utility installed for JSON parsing.


### Git: Shortcuts

- **Initialize a New Local Git Repository**:
  ```bash
  gcreate
  ```

- **Initialize a New Local Git Repository and Create a New GitHub Repository**:
  ```bash
  gcreate-remote [RepoName]
  ```

- **Add Files to Staging Area**:
  ```bash
  ga [FileName]
  ```

- **Commit Changes**:
  ```bash
  gc "Commit Message"
  ```

- **Push Changes to Origin**:
  ```bash
  gp [BranchName]
  ```

- **Pull Changes from Origin**:
  ```bash
  gpl
  ```

- **Check Git Status**:
  ```bash
  gs
  ```

- **Clone a Repository**:
  ```bash
  gcl [RepositoryURL]
  ```

- **List Branches**:
  ```bash
  gbr
  ```

- **Delete Branch**:
  ```bash
  gbrd [BranchName]
  ```

- **Force Delete Branch**:
  ```bash
  gbrD [BranchName]
  ```

- **Rename Branch**:
  ```bash
  gbrm [OldName] [NewName]
  ```

- **Force Rename Branch**:
  ```bash
  gbrM [OldName] [NewName]
  ```

- **Verbose List Branches**:
  ```bash
  gbrv
  ```

- **Visualize Git Log**:
  ```bash
  glg
  ```

- **See Differences**:
  ```bash
  gdf
  ```

- **Initialize Git Flow**:
  ```bash
  gfi
  ```

- **Start a New Feature Branch**:
  ```bash
  gfs [FeatureName]
  ```

- **Finish a Feature Branch**:
  ```bash
  gff [FeatureName]
  ```

- **Start a New Release Branch**:
  ```bash
  grs [ReleaseName]
  ```

- **Finish a Release Branch**:
  ```bash
  grf [ReleaseName]
  ```

- **Start a New Hotfix Branch**:
  ```bash
  ghs [HotfixName]
  ```

- **Finish a Hotfix Branch**:
  ```bash
  ghf [HotfixName]
  ```

- **Start a New Bugfix Branch**:
  ```bash
  gbs [BugfixName]
  ```

- **Finish a Bugfix Branch**:
  ```bash
  gbf [BugfixName]
  ```

- **Checkout to a Branch**:
  ```bash
  gco [BranchName]
  ```

- **Checkout to a Feature Task Branch**:
  ```bash
  gcft [TaskName]
  ```

- **Checkout to a Feature Branch**:
  ```bash
  gcf [FeatureName]
  ```

- **Checkout to a Release Branch**:
  ```bash
  gcr [ReleaseName]
  ```

- **Checkout to a Hotfix Branch**:
  ```bash
  gch [HotfixName]
  ```

- **Checkout to a Bugfix Branch**:
  ```bash
  gcb [BugfixName]
  ```

- **Checkout to the Develop Branch**:
  ```bash
  gcd
  ```

- **Checkout to the Master Branch**:
  ```bash
  gcm
  ```

- **Checkout to the Tests Branch**:
  ```bash
  gct
  ```

- **Checkout to the Prod Branch**:
  ```bash
  gcp
  ```

- **Checkout to the Preprod Branch**:
  ```bash
  gcpp
  ```

- **Stash Changes**:
  ```bash
  gst
  ```

- **List Stashed Changes**:
  ```bash
  gstl
  ```

- **Pop Stashed Changes**:
  ```bash
  gstp
  ```

- **Clear Stashed Changes**:
  ```bash
  gstc
  ```

- **Merge a Feature Task into Current Branch**:
  ```bash
  gmf [TaskName]
  ```

- **Merge Current Branch into Specified Branch**:
  ```bash
  gmergin [BranchName]
  ```

- **Update Multiple Branches (Develop, Master, Current)**:
  ```bash
  git-update
  ```

- **Push Multiple Branches (Develop, Master, Current) After MEP**:
  ```bash
  git-after-mep
  ```

- **Display Git Configuration Info**:
  ```bash
  ginfo
  ```

### Laravel: Shortcuts

- **Execute Artisan Command**:
  ```bash
  art [command]
  ```

- **Create Artisan Resources**:
  ```bash
  artm [type] [name]
  ```
  *Where `[type]` can be any of the `make` options like `controller`, `model`, `migration`, etc., and `[name]` is the desired name for the resource.*

- **Run Migrations**:
  ```bash
  artmig
  ```

- **Start Laravel Development Server**:
  ```bash
  artserve
  ```

- **Interact with Laravel Tinker**:
  ```bash
  arttink
  ```

- **Clear Various Laravel Caches**:
  ```bash
  artclean
  ```

### MacOS: Shortcuts

#### Tor

- **Activate TOR Proxy**:
  ```bash
  torStart
  ```
  This command sets up the proxy configuration on your Mac to use the local TOR instance and then starts the TOR service using Homebrew.

- **Deactivate TOR Proxy**:
  ```bash
  torStop
  ```
  This will disable the proxy configuration on your Mac and stop the TOR service that's been started with Homebrew.

- **Restart TOR Proxy**:
  ```bash
  torRestart
  ```
  This command is a combination of `torStop` and `torStart`, effectively restarting your TOR proxy setup.

- **Check TOR Exit Node Configuration**:
  ```bash
  torCheck
  ```
  This displays the current configuration values for your TOR exit node by reading the `/etc/torrc.exit` file.

- **Set TOR Entry Node**:
  ```bash
  torIn [country_code]
  ```
  *Where `[country_code]` is the desired entry node's country code.*  
  It sets the entry node for TOR to the specified country and then restarts the TOR service.

- **Set TOR Exit Node**:
  ```bash
  torOut [country_code]
  ```
  *Where `[country_code]` is the desired exit node's country code.*  
  It configures the exit node for TOR to use nodes from the specified country and then restarts the TOR service.

**Note**: These utilities are designed for macOS and use specific macOS commands for configuring network settings. Before using these commands, ensure that you have proper permissions, and be careful when editing configuration files. Always make backups before making any changes.

---

## Contributing
We welcome contributions! Whether you're adding new commands, improving existing ones, or fixing issues, your input enriches the BashMate experience. See the CONTRIBUTING.md for more details.

---

## License
This project is licensed under the CC BY-NC - see the LICENSE file for details.