#!/usr/bin/env osascript
# compose an email and attachment with Mail
# usage: macmailto <address> <subject> <body> <attach>

on run {theAddress, theSubject, theBody, theAttachment}
# 	http://stackoverflow.com/a/10065338/408556
	tell application "Mail"
		set theNewMessage to make new outgoing message with properties {subject:theSubject, content:theBody & return & return, visible:true}
		tell theNewMessage
			set visibile to true
			make new to recipient at end of to recipients with properties {address:theAddress}
			try
				set theFile to POSIX file theAttachment as alias
				make new attachment with properties {file name:theFile} at after the last word of the last paragraph
				set message_attachment to 0
			on error errmess -- oops
				log errmess -- log the error
				set message_attachment to 1
			end try
			log "message_attachment = " & message_attachment
		end tell
	end tell
end run
