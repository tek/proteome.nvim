[![Join the chat at https://gitter.im/tek/proteome.nvim](https://badges.gitter.im/tek/proteome.nvim.svg)](https://gitter.im/tek/proteome.nvim?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This plugin assists in working on multiple projects in a single neovim
instance, allowing to change the current working directory according to a
defined set of projects, and providing additional functionality like project
specific configuration, ctags handling and a git history.

# Setup

[![Join the chat at https://gitter.im/tek/proteome.nvim](https://badges.gitter.im/tek/proteome.nvim.svg)](https://gitter.im/tek/proteome.nvim?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
This repository is only a neovim remote plugin wrapper for the python
project containing the main code, which must be installed on your pythonpath:

```
pip install proteome
```

**Note**: You need to have the newest version of `libgit2` installed in
your system before running the above command.
If your system doesn't have bleeding edge package management, you'll also have
to adapt the version of `pygit2` to the libgit2 version (before installing
`proteome`).

**Note**: Python 3.5.1 is required to run the plugin.

For example, on Ubuntu Wily, working packages are:
```
apt-get install libgit2-22
pip install 'pygit2==0.22.*'
```

After installation, regularly install the nvim plugin and execute
`:UpdateRemotePlugins`.

# General functionality
The core concept is the management of the current project, its dependencies on
the local file system and their project types.
The most basic property being manipulated is the working dir, which can be switched
to one of the projects in the set.
The main project is always present, additional ones can be added either during
startup or dynamically at runtime.

### Startup
The regular initialization flow is:

* Proteome starts during the `after/plugin/` vim phase.

* The [main project](#main-project) is determined.

* Based on the result of that, [project specific vim config](#config) is
  loaded.  This is where dependency projects should be added.

* The project specific config is applied and the initial state is created.

* The *after* part of the project config is loaded.

* In the final initialization phase, plugins perform finishing tasks.

### Commands

Projects can be configured in several ways, explained below, and added with the
`ProAdd` command.

The argument to `ProAdd` must be an identifier in the shape of either
`type/name` or `name`, where `type` is an optional identifier used for several
functions, generally the project's main language.
Optionally, a json object can be passed to configure the project's parameters.

The `ProNext` and `ProPrev` commands allow cycling through
the set of projects, changing `cwd` to the currently active project's root.

The `ProSave` command is intended to be executed with `:wall`, depending on the
user's workflow, as the plugins perform several tasks that rely on that.
If you have a 'save all' mapping, you should combine it with this.

`ProShow` prints a short overview of added projects.

`ProTo` activates a project, either by index or by name.

`ProClone` fetches a git repository into a base dir, using the main type, and
adds it as if `ProAdd` was executed.

#### Examples
```
ProAdd python/proteome
```

Tries to look up the project `proteome` of type `python`, first in the [json
config](#json-config), then the [type indexed base dirs](#type-indexed) and
finally the [explicitly typed dirs](#explicitly-typed).

```
ProAdd rails/mysite { "root": "/projects/mysite", "types": ["jade", "ruby"] }
```

Adds the project `mysite` of type `rails`, if the root dir exists, with
additional project types `jade` and `ruby` (see [Config plugin](#config)).

```
ProAdd neovim
```
Tries to look up `neovim` as project name in the json config, then uses the
main project type to search in type dirs like in the first example.

# Configuration
General config options that should be set:

### Plugins
By default, only the features described above are available. By defining this variable, additional (including custom) plugins can be activated.

```viml
let g:proteome_plugins = [
      \ 'proteome.plugins.ctags',
      \ 'proteome.plugins.history',
      \ 'proteome.plugins.config',
      \ ]
```

### Project base dirs
There are two kinds of base directory where proteome looks up a project identifier:

#### Type indexed
In type indexed directories, matching projects are located at the path
`basedir/type/name`.

```viml
let g:proteome_base_dirs = ['~/projects', '/data/projects']
```

Lookup for `type/name` then checks `~/projects/type/name` and
`/data/projects/type/name`.

#### Explicitly typed
Type base dirs are used to look up only the types defined in the dict's values
and match subdirs of the corresponding keys with the name of the given project.
```viml
let g:proteome_type_base_dirs = {
      \ '~/.config/nvim/bundle': ['vim', 'nvim'],
      \ }
```

Lookup for `vim/name` then checks `~/.config/nvim/bundle/name`.

### json config
Additionally, projects can be configured explicitly in json files. The variable
needs to point to a directory; all contained json files will be read.
```viml
let g:proteome_config_path = '~/.config/projects'
```
The config file format is a list of json objects like so:
```json
[
  {
    "name": "proteome",
    "type": "python",
    "root": "/projects/python/proteome"
  }
]
```

### Main Project
During startup, the principal project that's being worked on is determined
automatically, unless the variable `proteome_main_project` is set (and
optionally `proteome_main_project_type`).

Automatic discovery compares the current directory to the base dir variables
described in [Project Base Dirs](#project-base-dirs) above and extracts name
and type from the path.

This information is then used by the [Config Plugin](#config) described below.

If only a name is specified to `ProAdd`, the main project's type is used as
fallback.

# Plugins

The elements of the `proteome_plugins` variable should denote a python module
that contains a `Plugin` class inheriting the
`proteome.state.ProteomeComponent` class.
There are three plugins present in the project:

## Config

Loads extra vim config from all runtimepaths based on the current project's
parameters, to run project type specific global configuration.
The location of the loaded files is every runtimepath directory's subdirectories
`project` and `project_after` (e.g. `~/.config/nvim/project_after`).
This is overridable via `g:proteome_config_project{,_after}_dir`.

For a project
named `mysite` with the main type `rails` and additional type `ruby`, the order
is:

* `project/rails.vim`
* `project/ruby.vim`
* `project/rails/mysite.vim`
* `project/all/*.vim`

and in the *after* phase, the same paths under `project_after`.

## Ctags

Generates ctags files in all projects when calling the `ProSave` command and
adds the `.tags` file in each project root to the `tags` option.
The languages used when scanning are the main project type and the optional
`langs` list parameter.

## History

```vim
let g:proteome_history_base = '~/tmp/nvim_history'
```

Creates bare git repositories for each project at
`{g:proteome_history_base}/type__name`, where a snapshot of the current project
state is commited every time `ProSave` is executed.
This provides a separate persistent undo history with git comfort without using
the project's regular git repository.

**Note**: This feature is pretty experimental, so don't be surprised if some
actions fail, especially the *pick* feature.

Only projects with the config attribute `"history": true` are considered. If
all projects should get a history, `let g:proteome_all_projects_history = 1`.
In the latter case, projects that don't have a type (like the fallback project
used for any dir) are excluded unless explicitly allowed.

Several commands for examining the history and checking out previous states are
provided:

`ProHistoryPrev` and `ProHistoryNext` check out the current project's parent
and child commits. Currently, only the whole project can be checked out, but
this will be provided for single files later.

`ProHistoryBrowse` loads a scratch buffer in a new tab and fills it with the
history, displaying the diff of the currently selected commit.
`j` and `k` are mapped to cycling up and down. Pressing `<cr>` checks out the
currently displayed commit.
`p` and `r` both try to revert the selected commit only, using `patch` and `git
revert` respectively. This can easily fail though, if the patch can't be
applied to the current working tree.

This is pretty preliminary, more features should be supplied soon.

## License

Copyright (c) Torsten Schmits. Distributed under the terms of the [MIT License][1].

[1]: http://opensource.org/licenses/MIT 'mit license'
