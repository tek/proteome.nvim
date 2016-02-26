function! s:report_failure(err) abort "{{{
  echom a:err
  echohl ErrorMsg
  echo 'rplugin/proteome not available, check the log'
  echohl None
endfunction "}}}

try
  ProteomeStart
catch
  autocmd VimEnter * call <sid>report_failure(v:exception)
endtry
