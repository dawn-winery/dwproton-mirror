##
## 7zip
##

$(eval $(call rules-source,sevenzip,$(SRCDIR)/steamrtdeps/7zip))
$(eval $(call rules-common,sevenzip,x86_64,unix))

SEVENZIP_ALONE2 := CPP/7zip/Bundles/Alone2

$(OBJ)/.sevenzip-x86_64-build:
	+$(MAKE) -C $(SEVENZIP_SRC)/$(SEVENZIP_ALONE2) -f makefile.gcc \
		O=$(SEVENZIP_x86_64_OBJ) IS_X64=1
	touch $@

$(OBJ)/.sevenzip-x86_64-dist:
	mkdir -p $(DST_DIR)/utils
	install -m 755 $(SEVENZIP_x86_64_OBJ)/7zz $(DST_DIR)/utils/7zz
	touch $@

all-dist: sevenzip
