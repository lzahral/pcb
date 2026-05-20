/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./assets/scss/style.scss":
/*!********************************!*\
  !*** ./assets/scss/style.scss ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

                eval("__webpack_require__.r(__webpack_exports__);\n// extracted by mini-css-extract-plugin\n\n\n//# sourceURL=webpack://cuba/./assets/scss/style.scss?");

                /***/
            })

        /******/
    });
/************************************************************************/
/******/ 	// The require scope
/******/ 	var __webpack_require__ = {};
/******/
/************************************************************************/
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if (typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
                /******/
            }
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
            /******/
        };
        /******/
    })();
/******/
/************************************************************************/
/******/
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./assets/scss/style.scss"](0, __webpack_exports__, __webpack_require__);
    /******/
    /******/
})()
    ;

// ------------------------------------------------------------
// PCB Color + Silkscreen Logic (custom code)
// ------------------------------------------------------------
document.addEventListener('DOMContentLoaded', function () {

  // همه رنگ‌های PCB
  const pcbRadios = document.querySelectorAll('input[name="PCB_color"]');

  // چاپ‌ها
  const silkWhite = document.getElementById('silk-white');
  const silkBlack = document.getElementById('silk-black');

  // آیدی‌ها را چک کنیم (برای جلوگیری از null error)
  if (!pcbRadios.length || !silkWhite || !silkBlack) {
    console.error("PCB or silkscreen fields not found in DOM");
    return;
  }

  // از بین بردن loop: فقط PCB تصمیم می‌گیرد
  function applySilkscreen(pcbColor) {

    const colorsWhiteSilk = ['green', 'purple', 'red', 'yellow', 'blue']; 
    // سازگار با name/value رادیوهای شما

    if (pcbColor === 'white') {
      // PCB سفید → چاپ مشکی
      silkBlack.disabled = false;
      silkBlack.checked = true;

      silkWhite.disabled = true;
      silkWhite.checked = false;
    }
    else if (pcbColor === 'black') {
      // PCB مشکی → چاپ سفید
      silkWhite.disabled = false;
      silkWhite.checked = true;

      silkBlack.disabled = true;
      silkBlack.checked = false;
    }
    else if (colorsWhiteSilk.includes(pcbColor)) {
      // رنگ‌های رنگی → چاپ سفید
      silkWhite.disabled = false;
      silkWhite.checked = true;

      silkBlack.disabled = true;
      silkBlack.checked = false;
    }

    // ارسال رویداد برای هر سیستم قیمت‌دهی / فرم
    silkWhite.dispatchEvent(new Event('change', { bubbles: true }));
   silkBlack.dispatchEvent(new Event('change', { bubbles: true }));
  }


  // وقتی PCB تغییر می‌کند
  pcbRadios.forEach(radio => {
    radio.addEventListener('change', function () {
      applySilkscreen(this.value);
    });
  });

  // حالت اولیه (مثلاً هنگام edit فرم)
  const initial = document.querySelector('input[name="PCB_color"]:checked');
  if (initial) applySilkscreen(initial.value);

});




// Base Materials' Layers 
const allowedLayersForMaterial = {
    "fr4": [1, 2, 4],
    "flex": [1, 2, 4],
    "aluminum": [1],
    "copper-core": [1],
    "rogers": [2],
    "PTFE": [2]
};

const layerOptions = document.querySelectorAll(".layer-option");
const materialRadios = document.querySelectorAll('input[name="base_material"]');

function showLayersForMaterial(material) {
    const allowed = allowedLayersForMaterial[material];

    layerOptions.forEach(opt => {
        opt.classList.add("hidden");
        opt.querySelector("input").checked = false;
    });

    allowed.forEach(num => {
        const el = document.querySelector(`.layer-option[data-layer="${num}"]`);
        if (el) el.classList.remove("hidden");
    });

    const first = allowed[0];
    document.querySelector(`input[name="layers"][value="${first}"]`).checked = true;
}

materialRadios.forEach(radio => {
    radio.addEventListener("change", () => {
        showLayersForMaterial(radio.id);
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const selected = document.querySelector('input[name="base_material"]:checked');
    if (selected) showLayersForMaterial(selected.id);
});
document.addEventListener("DOMContentLoaded", () => {
    const radios = document.querySelectorAll('input[name="base_material"]');

    const el = (id) => document.getElementById(id);

    const ui = {
        substrateWrapper: el("substrate-wrapper"),
        green: el("id-green"),
        purple: el("id-purple"),
        red: el("id-red"),
        blue: el("id-blue"),
        ENIG: el("id-ENIG"),
        ENIG_input: el("in-ENIG"),
        HASL: el("id-HASL"),
        HASL_input: el("in-HASL"),           // فرض کردم input مربوط به HASL این id رو داره
        LeadFree_HASL: el("id-LeadFree_HASL"),
        OSP: el("id-OSP"),
        goldWrapper: el("gold_thickness"),
    };

    const hide = (items) => items.forEach(i => i?.classList.add("hidden"));
    const show = (items) => items.forEach(i => i?.classList.remove("hidden"));

    // rules
    const GOLD_REQUIRED_MATERIALS = new Set(["flex", "rogers", "ptfe"]);
    const HASL_AUTO_MATERIALS = new Set(["aluminum"]);

    function getSelectedValue() {
        const selected = document.querySelector('input[name="base_material"]:checked');
        return selected ? selected.value : null;
    }

    function updateUI() {
        const value = getSelectedValue();
        if (!value) return;

        const isFlex = value === "flex";
        const isFR4 = value === "fr4";
        const isAl = value === "aluminum";
        const isRogers = value === "rogers";
        const isPtfe = value === "ptfe";
        const isCopper = value === "copper";

        const goldRequired = GOLD_REQUIRED_MATERIALS.has(value);
        const haslRequired = HASL_AUTO_MATERIALS.has(value);

        const colors = [ui.green, ui.purple, ui.red, ui.blue];

        // substrate
        ui.substrateWrapper.classList.toggle("hidden", !isFlex);

        // colors
        isFlex ? hide(colors) : show(colors);

        // OSP
        ui.OSP.classList.toggle(
            "hidden",
            isFR4 || isFlex || isAl || isRogers || isPtfe
        );

        // HASL auto select
        if (haslRequired) {
            ui.HASL_input.checked = true;
        }

        ui.HASL.classList.toggle("hidden", isFlex);
        ui.LeadFree_HASL.classList.toggle("hidden", isFlex);

        // ENIG auto select for special materials
        if (goldRequired) {
            ui.ENIG_input.checked = true;
        }
        
        // GOLD visibility depends on ENIG state + material
        const showGold = goldRequired && ui.ENIG_input.checked;
        ui.goldWrapper.classList.toggle("hidden", !showGold);
    }

    // events
    radios.forEach(r => r.addEventListener("change", updateUI));
    ui.ENIG_input.addEventListener("change", updateUI);

    // init
    updateUI();
});
// document.addEventListener("DOMContentLoaded", function () {
//     const radios = document.querySelectorAll('input[name="base_material"]');
//     const substrateWrapper = document.getElementById("substrate-wrapper");
//     const green = document.getElementById("id-green");
//     const purple = document.getElementById("id-purple");
//     const red = document.getElementById("id-red");
//     const blue = document.getElementById("id-blue");
//     const ENIG = document.getElementById("id-ENIG");
//     const ENIG_input = document.getElementById("in-ENIG");
//     const HASL = document.getElementById("id-HASL");
//     const LeadFree_HASL = document.getElementById("id-LeadFree_HASL");
//     const OSP = document.getElementById("id-OSP");
//     const goldWrapper = document.getElementById("gold_thickness");

//     console.log(green)
//     function updateSubstrateVisibility() {
//         const selected = document.querySelector('input[name="base_material"]:checked');
//         if (selected.value === "flex") {
//             substrateWrapper.classList.remove("hidden");
//             green.classList.add("hidden");
//             purple.classList.add("hidden");
//             red.classList.add("hidden");
//             blue.classList.add("hidden");
//         } else {
//             substrateWrapper.classList.add("hidden");
//             green.classList.remove("hidden");
//             purple.classList.remove("hidden");
//             red.classList.remove("hidden");
//             blue.classList.remove("hidden");
//         }
//         if (selected.value === "fr4") {
//             OSP.classList.add("hidden");
//         } else if (selected.value === "flex") {
//             OSP.classList.add("hidden");
//             HASL.classList.add("hidden");
//             LeadFree_HASL.classList.add("hidden");
//             ENIG_input.checked = true;
//             goldWrapper.classList.remove("hidden");
//         } else {
//             substrateWrapper.classList.add("hidden");
//             goldWrapper.classList.add("hidden");
//             green.classList.remove("hidden");
//             purple.classList.remove("hidden");
//             red.classList.remove("hidden");
//             blue.classList.remove("hidden");
//         }
//     }

//     radios.forEach(radio => {
//         radio.addEventListener("change", updateSubstrateVisibility);
//     });

//     updateSubstrateVisibility();
// });
document.addEventListener("DOMContentLoaded", function () {

    const checkbox = document.getElementById("change");
    const panel_grid = document.getElementById("panel_grid");
    const dimension = document.getElementById("dimension");

    checkbox.addEventListener("change", handleSwitch);

    function handleSwitch(e) {
        if (e.target.checked) {
            panel_grid.classList.remove("hidden");
        } else {
            panel_grid.classList.add("hidden");
        }
    }
    const radios = document.querySelectorAll('input[name="surface_finish"]');
    const goldWrapper = document.getElementById("gold_thickness");
    function updateSubstrateVisibility() {
        const selected = document.querySelector('input[name="surface_finish"]:checked');
        if (selected && selected.value === "ENIG") {
            goldWrapper.classList.remove("hidden");
        } else {
            goldWrapper.classList.add("hidden");
        }
    }
    radios.forEach(radio => {
        radio.addEventListener("change", updateSubstrateVisibility);
    });

    updateSubstrateVisibility();
});
