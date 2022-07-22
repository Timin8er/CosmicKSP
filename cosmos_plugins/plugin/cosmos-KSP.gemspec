# encoding: ascii-8bit

spec = Gem::Specification.new do |s|
  s.name = 'cosmos-KSP'
  s.summary = 'KSP Connection'
  s.description = <<-EOF
    This plugin adds the KSP targets and configuration
  EOF
  s.authors = ['Tim Polnow']
  s.homepage = 'https://github.com/Timin8er/CosmicKSP'

  s.platform = Gem::Platform::RUBY

  if ENV['VERSION']
    s.version = ENV['VERSION'].dup
  else
    time = Time.now.strftime("%Y%m%d%H%M%S")
    s.version = '0.0.0' + ".#{time}"
  end
  s.licenses = ['AGPL-3.0-only', 'Nonstandard']

  s.files = Dir.glob("{targets,lib,procedures,tools,microservices}/**/*") + %w(Rakefile LICENSE.txt README.md plugin.txt)
end
