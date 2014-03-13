# Equivalent to shell "which", returning the first occurence of its
# argument, cmd, on the PATH:
proc which {cmd} {
    foreach dir [split $::env(PATH) :] {
        set fqpn $dir/$cmd
        if { [file exists $fqpn] } {
            return $fqpn
        }
    }
}

# True if 'path' exists and is a symbolic link:
proc is_link {path} {
    return [file exists $path] && [string equal [file type $path] link]
}

# Chases a symbolic link until it resolves to a file that
# isn't a symlink:
proc chase {link} {
    set max_depth 10 ; # Sanity check
    set i 0
    while { [is_link $link] && $i < $max_depth } {
        set link [file link $link]
        incr i
    }
    if { $i >= $max_depth } {
        return -code error "maximum link depth ($max_depth) exceeded"
    }
    return $link
}

# Returns the "true home" of its argument, a command:
proc get_real_home {cmd} {
    set utgt [chase [which $cmd]]    ; # Ultimate target
    set home [file dirname $utgt]    ; # Directory containing target
    if { [string equal bin [file tail $home]] } {
        set home [file dirname $home]
    }
    return $home
}
