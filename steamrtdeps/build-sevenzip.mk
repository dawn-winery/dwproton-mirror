##
## 7zip
##

$(eval $(call rules-source,sevenzip,$(SRCDIR)/steamrtdeps/7zip))
$(eval $(call rules-common,sevenzip,x86_64,unix))
$(eval $(call rules-common,sevenzip,aarch64,unix))

SEVENZIP_ALONE2 := CPP/7zip/Bundles/Alone2

SEVENZIP_x86_64_MAKE_ARGS := IS_X64=1
SEVENZIP_aarch64_MAKE_ARGS := IS_ARM64=1 USE_ASM=1 ASM_FLAGS=-Wno-unused-macros

$(OBJ)/.sevenzip-x86_64-build:
	+env $(SEVENZIP_x86_64_ENV) $(MAKE) -C $(SEVENZIP_SRC)/$(SEVENZIP_ALONE2) -f makefile.gcc \
		O=$(SEVENZIP_x86_64_OBJ) $(SEVENZIP_x86_64_MAKE_ARGS)
	touch $@

$(OBJ)/.sevenzip-aarch64-build:
	+env $(SEVENZIP_aarch64_ENV) $(MAKE) -C $(SEVENZIP_SRC)/$(SEVENZIP_ALONE2) -f makefile.gcc \
		O=$(SEVENZIP_aarch64_OBJ) $(SEVENZIP_aarch64_MAKE_ARGS)
	touch $@

$(OBJ)/.sevenzip-x86_64-dist:
	mkdir -p $(DST_DIR)/utils
	install -m 755 $(SEVENZIP_x86_64_OBJ)/7zz $(DST_DIR)/utils/7zz
	touch $@

$(OBJ)/.sevenzip-aarch64-dist:
	mkdir -p $(DST_DIR)/utils
	install -m 755 $(SEVENZIP_aarch64_OBJ)/7zz $(DST_DIR)/utils/7zz
	touch $@

all-dist: sevenzip
