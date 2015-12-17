This plugin assists in working on multiple projects in a single neovim
instance, allowing to change the current working directory according to a
defined set of projects, and providing additional functionality like project
specific configuration, ctags handling and a git history.

# Setup
This repository is only a neovim remote plugin wrapper for the python
project containing the main code, which must be installed on your pythonpath:

```
pip install proteome
```

# General functionality
The core concept is the management of the current project, its dependencies on
the local file system and their project types.
The most basic property being manipulated is the working dir, which can be switched
to one of the projects in the set.

Projects can be configured in several ways, explained below, and added with the
`ProAdd` command. The `ProNext` and `ProPrev` commands allow cycling through
the set of projects, changing `cwd` to the currently active project's root.

The argument to `ProAdd` must be an identifier in the shape of either
`type/name` or `name`, where `type` is an optional identifier used for several
functions, generally the project's main language.
Optionally, a json object can be passed to configure the project's parameters.

#### Examples
`Pro Add python/proteome`

Tries to look up the project `proteome` of type `python`, first in the json
config, then the type indexed base dirs and finally the explicitly typed dirs
(see next section).

`ProAdd rails/mysite { "root": "/projects/mysite", "types": ["jade", "ruby"] }`

Adds the project `mysite` of type `rails`, if the root dir exists, with
additional project types `jade` and `ruby` (see the `config` plugin).


The `ProSave` command is intended to be executed with `:wall`, depending on the
user's workflow, as the plugins perform several tasks that rely on that.
If you have a 'save all' mapping, you should combine it with this.


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

For a project
named `mysite` with the main type `rails` and additional type `ruby`, the order
is:

* `project/rails.vim`
* `project/ruby.vim`
* `project/rails/mysite.vim`
* `project/all/*.vim`

and shortly after that, the same paths under `project_after`.

At the moment, the `after` files are called one second later, but this may be
replaced by a better method later. The reason why this isn't done at the
regular `plugin/` sourcing time is that remote plugins are initialized late.

## Ctags

Generates ctags files in all projects when calling the `ProSave` command and
adds the `.tags` file in each project root to the `tags` option.
The languages used when scanning are the main project type and the optional
`langs` list parameter.

## history

```vim
let g:proteome_history_base = '~/tmp/nvim_history'
```

Creates bare git repositories for each project at
`{g:proteome_history_base}/type__name`, where a snapshot of the current project
state is commited every time `ProSave` is executed.
This provides a separate persistant undo history with git comfort without using
the project's regular git repository.