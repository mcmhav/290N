#RMFILES = pan.* *.trail f13 f18

#clean:
#	rm -f $(RMFILES)
#	clear

# If the first argument is "run"...
ifeq (push,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  MESSAGE := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(MESSAGE):;@:)
endif

push:
#	rm -f $(RMFILES)
	git commit -am $(MESSAGE) && git pull && git push

query:
	cd scripts && clear && rm -f ../query.log && python query.py

understandQuery:
	cd scripts && clear && python understandQueryLog.py
