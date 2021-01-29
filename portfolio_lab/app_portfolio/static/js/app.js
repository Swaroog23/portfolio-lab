document.addEventListener("DOMContentLoaded", function () {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;


      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
        if (el.dataset.id === 3) {

          // first_slide = el.dataset.id === "1"
          // chosen_categories === first_slide.children.classList("selected");
          // console.log(chosen_categories, first_slide);
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function (e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];
      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
          this.stepOneCheckboxEvent();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */

    updateForm() {
      this.stepOneCheckboxEvent();
      this.$step.innerText = this.currentStep;
      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");
        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
        if (this.currentStep === 3) {
          let selectedCategoriesArray = [];
          this.slides[6].parentElement.children[0].querySelectorAll("div.selected > label > input").forEach(item => {
            selectedCategoriesArray.push(item.value)
          })

          let institutions = this.slides[6].querySelectorAll(".form-group--checkbox");
          console.log(selectedCategoriesArray)
          institutions.forEach(institute => {
            if (!institute.classList.contains(selectedCategoriesArray)) {
              institute.style.display = "none";
            }
          })
        }
      });
      this.checkIfRadioChecked();

      if (this.currentStep === 4) {
        let buttonStepFour = this.$form.querySelector(".form--steps-container > form > [data-step='4']").querySelector(".next-step");
        buttonStepFour.addEventListener("click", e => {
          let firstFormColumn = buttonStepFour.parentElement.previousElementSibling.firstElementChild;
          let streetName = firstFormColumn.children[1].querySelector("input").value;
          let cityName = firstFormColumn.children[2].querySelector("input").value;
          let postalCode = firstFormColumn.children[3].querySelector("input").value;
          let phoneNumber = firstFormColumn.children[4].querySelector("input").value;

          let secondFormColumn = buttonStepFour.parentElement.previousElementSibling.lastElementChild;
          let pickupDate = secondFormColumn.children[1].querySelector("input").value;
          let pickupHour = secondFormColumn.children[2].querySelector("input").value;
          let additionalInfo = secondFormColumn.children[3].querySelector("textarea").value;

          let chosenOrganization = buttonStepFour.parentElement.parentElement.previousElementSibling.querySelector("div.selected > label > span.description > div.title").innerText;
          let amountOfBags = buttonStepFour.parentElement.parentElement.previousElementSibling.previousElementSibling.querySelector("div.form-group--inline > label > input").value;
          let itemsToDonate = [];
          this.$form.querySelector(".form--steps-container > form > [data-step='1']").querySelectorAll("div.selected > label > span.description").forEach(
            item => {
              itemsToDonate.push(item.innerText)
            }
          );


          if (this.currentStep === 5) {
            let finalizationForm = this.$form.querySelector(".form--steps-container > form > [data-step='5']").querySelector("div.summary");
            let bagsAndOrganisationInfo = finalizationForm.querySelector("div.form-section").querySelector("ul");
            if (amountOfBags === "1") {
              bagsAndOrganisationInfo.firstElementChild.querySelector("span.summary--text").innerText += `1 worek ${itemsToDonate}`
            } else if (amountOfBags > 1 && amountOfBags < 5) {
              bagsAndOrganisationInfo.firstElementChild.querySelector("span.summary--text").innerText += `${amountOfBags} worki ${itemsToDonate}`
            } else {
              bagsAndOrganisationInfo.firstElementChild.querySelector("span.summary--text").innerText += `${amountOfBags} worków ${itemsToDonate}`
            }
            bagsAndOrganisationInfo.lastElementChild.querySelector("span.summary--text").innerText = `Dla organizacji ${chosenOrganization}`
            let deliveryPickupInfo = finalizationForm.querySelectorAll("div.form-section--column");
            console.log(deliveryPickupInfo)
            let deliveryPickupAddress = deliveryPickupInfo[0].querySelector("ul").children;
            deliveryPickupAddress[0].innerText = streetName;
            deliveryPickupAddress[1].innerText = cityName;
            deliveryPickupAddress[2].innerText = postalCode;
            deliveryPickupAddress[3].innerText = phoneNumber;

            let deliveryPickupDateTime = deliveryPickupInfo[1].querySelector("ul").children;
            deliveryPickupDateTime[0].innerText = pickupDate;
            deliveryPickupDateTime[1].innerText = pickupHour;
            if (additionalInfo) {
              deliveryPickupDateTime[2].innerText = additionalInfo;
            } else {
              deliveryPickupDateTime[2].innerText = "Brak uwag"
            }

          }
        })

      }

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

    }

    checkIfRadioChecked() {
      let radioCheboxes = this.$form.querySelector(".form--steps-container > form > [data-step='3']").querySelectorAll("div.form-group--checkbox > label > input");
      radioCheboxes.forEach(checkbox => {
        if (checkbox.checked) {

          checkbox.parentElement.parentElement.classList.add("selected");
        }

      });
    }
    stepOneCheckboxEvent() {
      let checkboxes = this.$form.querySelector(".form--steps-container > form > [data-step='1']").querySelectorAll("div.form-group--checkbox > label > input");
      checkboxes.forEach(elem => {
        elem.addEventListener("change", event => {

          if (elem.checked) {
            elem.parentElement.parentElement.classList.add("selected");
          } else {
            elem.parentElement.parentElement.classList.remove("selected");
          }
        })
      })
    };
    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});