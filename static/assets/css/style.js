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

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The require scope
/******/ 	var __webpack_require__ = {};
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./assets/scss/style.scss"](0, __webpack_exports__, __webpack_require__);
/******/ 	
/******/ })()
;

// ------------------------------------------------------------
// PCB Color + Silkscreen Logic (custom code)
// ------------------------------------------------------------
document.addEventListener('DOMContentLoaded', function() {

  const pcbRadios = document.querySelectorAll('input[name="pcb_color"]');
  const silkWhite = document.getElementById('silk-white');
  const silkBlack = document.getElementById('silk-black');

  // تابع تنظیم وضعیت رنگ چاپ (فعال/غیرفعال + انتخاب خودکار)
  function setSilkscreen(color) {

    if (color === 'white') {
      silkWhite.checked = true;
      silkWhite.disabled = false;
      silkBlack.checked = false;
      silkBlack.disabled = true;   // غیرفعال کردن Black
    } 
    else if (color === 'black') {
      silkBlack.checked = true;
      silkBlack.disabled = false;
      silkWhite.checked = false;
      silkWhite.disabled = true;   // غیرفعال کردن White
    }
    else {
      // رنگ‌های دیگر PCB → فقط سفید فعال
      silkWhite.checked = true;
      silkWhite.disabled = false;
      silkBlack.checked = false;
      silkBlack.disabled = true;
    }
  }

  // وابستگی رنگ چاپ به رنگ PCB
  pcbRadios.forEach(radio => {
    radio.addEventListener('change', () => {
      const color = radio.value;
      if (color === 'black') setSilkscreen('white');
      else if (color === 'white') setSilkscreen('black');
      else setSilkscreen('white');
    });
  });

  // تغییر دستی کاربر روی Silkscreen
  silkWhite.addEventListener('change', function () {
    if (this.checked) setSilkscreen('white');
  });

  silkBlack.addEventListener('change', function () {
    if (this.checked) setSilkscreen('black');
  });

  // حالت اولیه هنگام بارگذاری
  if (silkWhite.checked) setSilkscreen('white');
  if (silkBlack.checked) setSilkscreen('black');

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

    // پنهان کردن همه لایه‌ها
    layerOptions.forEach(opt => {
        opt.classList.add("hidden");
        opt.querySelector("input").checked = false;
    });

    // نمایش لایه‌های مجاز
    allowed.forEach(num => {
        const el = document.querySelector(`.layer-option[data-layer="${num}"]`);
        if (el) el.classList.remove("hidden");
    });

    // انتخاب اولین لایه مجاز
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


// document.addEventListener('DOMContentLoaded', function () {
//     const baseMaterialRadios = document.querySelectorAll('input[name="base_material"]');
//     const flexSubstrateGroup = document.querySelector('.flex-substrate-group');

//     function updateUIForBaseMaterial(selectedMaterialId) {

//         if (selectedMaterialId === 'flex') {
//             flexSubstrateGroup.classList.remove('hidden');
//         } else {
//             flexSubstrateGroup.classList.add('hidden');

//             const defaultSubstrate = document.getElementById('flex-substrate-none');
//             if (defaultSubstrate) {
//                 defaultSubstrate.checked = true;
//             }
//         }
//     }

//     // لیسنر انتخاب متریال
//     baseMaterialRadios.forEach(radio => {
//         radio.addEventListener('change', function () {
//             if (this.checked) {
//                 updateUIForBaseMaterial(this.id); // چون idها را در allowedLayersForMaterial هم استفاده می‌کنی
//             }
//         });
//     });

//     // مقدار اولیه (اگر صفحه با گزینه‌ای شروع می‌شود)
//     const initiallyChecked = document.querySelector('input[name="base_material"]:checked');
//     if (initiallyChecked) {
//         updateUIForBaseMaterial(initiallyChecked.id);
//     }
// });

document.addEventListener("DOMContentLoaded", function () {
    const radios = document.querySelectorAll('input[name="base_material"]');
    const substrateWrapper = document.getElementById("substrate-wrapper");
    const green = document.getElementById("id-green");
    const purple = document.getElementById("id-purple");
    const red = document.getElementById("id-red");
    const blue = document.getElementById("id-blue");
    console.log(green)
    function updateSubstrateVisibility() {
        const selected = document.querySelector('input[name="base_material"]:checked');
        if (selected && selected.value === "flex") {
            substrateWrapper.classList.remove("hidden");
            green.classList.add("hidden");
            purple.classList.add("hidden");
            red.classList.add("hidden");
            blue.classList.add("hidden");
        } else {
            substrateWrapper.classList.add("hidden");
            green.classList.remove("hidden");
            purple.classList.remove("hidden");
            red.classList.remove("hidden");
            blue.classList.remove("hidden");
        }
    }

    radios.forEach(radio => {
        radio.addEventListener("change", updateSubstrateVisibility);
    });

    updateSubstrateVisibility();
});
document.addEventListener("DOMContentLoaded", function () {
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
