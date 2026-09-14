(function () {
    "use strict";

    // ---- footer year ----
    var yearEl = document.getElementById("footerYear");
    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }

    // ---- language switcher dropdown ----
    var langToggle = document.getElementById("langToggle");
    var langMenu = document.getElementById("langMenu");

    if (langToggle && langMenu) {
        function closeLangMenu() {
            langMenu.hidden = true;
            langToggle.setAttribute("aria-expanded", "false");
        }

        function openLangMenu() {
            langMenu.hidden = false;
            langToggle.setAttribute("aria-expanded", "true");
        }

        langToggle.addEventListener("click", function (event) {
            event.stopPropagation();
            if (langMenu.hidden) {
                openLangMenu();
            } else {
                closeLangMenu();
            }
        });

        document.addEventListener("click", function (event) {
            if (!langMenu.hidden && !event.target.closest(".lang-switch")) {
                closeLangMenu();
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && !langMenu.hidden) {
                closeLangMenu();
                langToggle.focus();
            }
        });
    }
})();

(function () {
    "use strict";

    // ---- mobile nav drawer (the ONLY nav-toggle logic in this file) ----
    var toggleBtn = document.getElementById("navToggle");
    var closeBtn = document.getElementById("navClose");
    var nav = document.getElementById("siteNav");
    var overlay = document.getElementById("navOverlay");

    if (!toggleBtn || !nav || !overlay) return;

    function isOpen() {
        return nav.classList.contains("is-open");
    }

    function openNav() {
        nav.classList.add("is-open");
        overlay.classList.add("is-open");
        toggleBtn.setAttribute("aria-expanded", "true");
        document.body.style.overflow = "hidden";
    }

    function closeNav() {
        nav.classList.remove("is-open");
        overlay.classList.remove("is-open");
        toggleBtn.setAttribute("aria-expanded", "false");
        document.body.style.overflow = "";
    }

    toggleBtn.addEventListener("click", function () {
        isOpen() ? closeNav() : openNav();
    });

    if (closeBtn) {
        closeBtn.addEventListener("click", closeNav);
    }

    overlay.addEventListener("click", closeNav);

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && isOpen()) {
            closeNav();
            toggleBtn.focus();
        }
    });

    nav.addEventListener("click", function (event) {
        if (event.target.closest("a")) {
            closeNav();
        }
    });

    window.addEventListener("resize", function () {
        if (window.innerWidth > 860 && isOpen()) {
            closeNav();
        }
    });
})();

(function () {
    "use strict";

    // ---- fleet carousel (the ONLY carousel logic in this file — single-step version) ----
    function initFleetCarousel(root) {
        var viewport = root.querySelector(".fleet__viewport");
        var track = root.querySelector(".fleet__track");
        var cards = Array.prototype.slice.call(track.children);
        var prevBtn = root.querySelector(".fleet-arrow--prev");
        var nextBtn = root.querySelector(".fleet-arrow--next");
        var dotsWrap = root.querySelector(".fleet__dots");

        if (!cards.length) return;

        var index = 0;
        var perPage = 3;
        var maxIndex = 0;

        function getPerPage() {
            var w = window.innerWidth;
            if (w <= 640) return 1;
            if (w <= 1000) return 2;
            return 3;
        }

        function buildDots() {
            if (!dotsWrap) return;
            dotsWrap.innerHTML = "";
            for (var i = 0; i <= maxIndex; i++) {
                var dot = document.createElement("button");
                dot.type = "button";
                dot.className = "fleet__dot" + (i === index ? " is-active" : "");
                dot.setAttribute("aria-label", "Show car " + (i + 1));
                dot.addEventListener("click", (function (idx) {
                    return function () { goTo(idx); };
                })(i));
                dotsWrap.appendChild(dot);
            }
        }

        function updateDots() {
            if (!dotsWrap) return;
            var dots = dotsWrap.querySelectorAll(".fleet__dot");
            dots.forEach(function (d, i) {
                d.classList.toggle("is-active", i === index);
            });
        }

        function updateArrows() {
            if (prevBtn) prevBtn.disabled = index === 0;
            if (nextBtn) nextBtn.disabled = index === maxIndex;
        }

        function render(recomputeLayout) {
            var newPerPage = getPerPage();
            if (recomputeLayout || newPerPage !== perPage) {
                perPage = newPerPage;
                maxIndex = Math.max(0, cards.length - perPage);
                index = Math.min(index, maxIndex);
                buildDots();
            }

            var cardWidth = cards[0].getBoundingClientRect().width;
            var gap = parseFloat(getComputedStyle(track).gap || 20);
            var offset = index * (cardWidth + gap);
            track.style.transform = "translateX(-" + offset + "px)";

            updateArrows();
            updateDots();
        }

        function goTo(newIndex) {
            index = Math.max(0, Math.min(newIndex, maxIndex));
            render(false);
        }

        if (prevBtn) prevBtn.addEventListener("click", function () { goTo(index - 1); });
        if (nextBtn) nextBtn.addEventListener("click", function () { goTo(index + 1); });

        var startX = null;
        viewport.addEventListener("touchstart", function (e) {
            startX = e.touches[0].clientX;
        }, { passive: true });

        viewport.addEventListener("touchend", function (e) {
            if (startX === null) return;
            var deltaX = e.changedTouches[0].clientX - startX;
            if (Math.abs(deltaX) > 40) {
                goTo(deltaX < 0 ? index + 1 : index - 1);
            }
            startX = null;
        });

        var resizeTimer;
        window.addEventListener("resize", function () {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function () { render(true); }, 150);
        });

        render(true);
    }

    document.querySelectorAll(".fleet").forEach(initFleetCarousel);
})();

(function () {
    "use strict";

    // ---- contact forms (driver / investor) ----
    var tabs = document.querySelectorAll(".form-tab");
    var panels = document.querySelectorAll(".form-panel");

    tabs.forEach(function (tab) {
        tab.addEventListener("click", function () {
            var target = tab.getAttribute("data-target");

            tabs.forEach(function (t) { t.classList.toggle("is-active", t === tab); });
            panels.forEach(function (p) {
                var isTarget = p.id === target;
                p.hidden = !isTarget;
            });
        });
    });

    function clearErrors(form) {
        form.querySelectorAll(".field-error").forEach(function (el) { el.textContent = ""; });
        form.querySelectorAll(".field-input").forEach(function (el) { el.classList.remove("has-error"); });
    }

    function showErrors(form, errors) {
        Object.keys(errors).forEach(function (fieldName) {
            var input = form.querySelector('[name="' + fieldName + '"]');
            var errorEl = form.querySelector('[data-error-for="' + fieldName + '"]');
            var message = errors[fieldName][0] && errors[fieldName][0].message
                ? errors[fieldName][0].message
                : "Please check this field.";

            if (input) input.classList.add("has-error");
            if (errorEl) errorEl.textContent = message;
        });
    }

    function showBanner(form, kind, message) {
        var banner = form.querySelector(".form-banner");
        if (!banner) return;
        banner.className = "form-banner is-visible form-banner--" + kind;
        banner.textContent = message;
    }

    function hideBanner(form) {
        var banner = form.querySelector(".form-banner");
        if (!banner) return;
        banner.className = "form-banner";
        banner.textContent = "";
    }

    function initForm(form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            clearErrors(form);
            hideBanner(form);

            var submitBtn = form.querySelector(".contact-form__submit");
            if (submitBtn) submitBtn.disabled = true;

            fetch(form.action, {
                method: "POST",
                body: new FormData(form),
                headers: { "X-Requested-With": "XMLHttpRequest" },
            })
                .then(function (response) {
                    return response.json().then(function (data) {
                        return { ok: response.ok, data: data };
                    });
                })
                .then(function (result) {
                    if (result.ok && result.data.success) {
                        form.reset();
                        showBanner(form, "success", "Thanks — we've got your details and will be in touch shortly.");
                    } else {
                        showErrors(form, result.data.errors || {});
                        showBanner(form, "error", "Please fix the highlighted fields and try again.");
                    }
                })
                .catch(function () {
                    showBanner(form, "error", "Something went wrong sending this. Please try again in a moment.");
                })
                .finally(function () {
                    if (submitBtn) submitBtn.disabled = false;
                });
        });
    }

    document.querySelectorAll(".contact-form").forEach(initForm);
})();