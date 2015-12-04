guard :shell, all_on_start: true do
  watch(/riml\/(.*).riml$/) do |file, base|
    dirs = Dir.glob('riml/**/*/').join(':')
    dir = File.dirname(base)
    `mkdir -p autoload/#{dir}`
    `riml -c #{file} -o autoload/#{dir} -S #{dirs} -I #{dirs}`
  end
end
