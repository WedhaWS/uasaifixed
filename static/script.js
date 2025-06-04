class EnhancedFoodAkinator {
  constructor() {
    this.sessionId = null
    this.currentQuestion = null
    this.questionCount = 0
    this.maxQuestions = 40 // Dinaikkan dari 30 ke 40
    this.ingredientsCount = 0
    this.minIngredients = 10 // Dinaikkan dari 8 ke 10
    this.confirmedIngredients = []

    this.initializeElements()
    this.bindEvents()
    this.showWelcomeScreen()
  }

  initializeElements() {
    // Screens
    this.welcomeScreen = document.getElementById("welcome-screen")
    this.questionScreen = document.getElementById("question-screen")
    this.loadingScreen = document.getElementById("loading-screen")
    this.resultsScreen = document.getElementById("results-screen")
    this.noResultsScreen = document.getElementById("no-results-screen")

    // Buttons
    this.startBtn = document.getElementById("start-btn")
    this.yesBtn = document.getElementById("yes-btn")
    this.noBtn = document.getElementById("no-btn")
    this.playAgainBtn = document.getElementById("play-again-btn")
    this.tryAgainBtn = document.getElementById("try-again-btn")

    // Elements
    this.questionText = document.getElementById("question-text")
    this.questionCategory = document.getElementById("question-category")
    this.progressFill = document.getElementById("progress-fill")
    this.progressText = document.getElementById("progress-text")
    this.ingredientsCountEl = document.getElementById("ingredients-count")
    this.currentIngredients = document.getElementById("current-ingredients")
    this.recommendationsList = document.getElementById("recommendations-list")
    this.availableIngredients = document.getElementById("available-ingredients")
    this.totalQuestions = document.getElementById("total-questions")
    this.totalIngredients = document.getElementById("total-ingredients")
    this.totalRecipes = document.getElementById("total-recipes")
    this.ingredientsPreview = document.getElementById("ingredients-preview")
    this.loadingQuestions = document.getElementById("loading-questions")
    this.loadingIngredients = document.getElementById("loading-ingredients")
  }

  bindEvents() {
    if (this.startBtn) {
      this.startBtn.addEventListener("click", () => this.startGame())
    }
    if (this.yesBtn) {
      this.yesBtn.addEventListener("click", () => this.answerQuestion("yes"))
    }
    if (this.noBtn) {
      this.noBtn.addEventListener("click", () => this.answerQuestion("no"))
    }
    if (this.playAgainBtn) {
      this.playAgainBtn.addEventListener("click", () => this.restartGame())
    }
    if (this.tryAgainBtn) {
      this.tryAgainBtn.addEventListener("click", () => this.restartGame())
    }
  }

  showWelcomeScreen() {
    this.showScreen(this.welcomeScreen)
  }

  showScreen(screenElement) {
    // Sembunyikan semua screen
    document.querySelectorAll(".screen").forEach((screen) => {
      screen.classList.add("hidden")
    })

    // Tampilkan screen yang dipilih
    if (screenElement) {
      screenElement.classList.remove("hidden")
    }
  }

  async startGame() {
    this.showScreen(this.loadingScreen)
    this.updateLoadingStats(0, 0)

    try {
      const response = await fetch("/start_game", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      })

      const data = await response.json()

      if (data.question) {
        this.sessionId = data.session_id
        this.questionCount = data.question_count
        this.maxQuestions = data.max_questions
        this.ingredientsCount = data.ingredients_count
        this.minIngredients = data.min_ingredients
        this.currentQuestion = data.question
        this.confirmedIngredients = []

        setTimeout(() => {
          this.showQuestion()
        }, 1500)
      } else {
        this.showError("Gagal memulai permainan")
      }
    } catch (error) {
      console.error("Error starting game:", error)
      this.showError("Terjadi kesalahan saat memulai permainan")
    }
  }

  showQuestion() {
    if (this.questionText) {
      this.questionText.textContent = this.currentQuestion
    }
    this.updateProgress()
    this.updateQuestionCategory()
    this.showScreen(this.questionScreen)

    // Tampilkan preview ingredients jika sudah ada
    if (this.confirmedIngredients.length > 0) {
      if (this.ingredientsPreview) {
        this.ingredientsPreview.style.display = "block"
      }
      this.updateIngredientsPreview()
    } else {
      if (this.ingredientsPreview) {
        this.ingredientsPreview.style.display = "none"
      }
    }
  }

  updateProgress() {
    const progress = (this.questionCount / this.maxQuestions) * 100
    if (this.progressFill) {
      this.progressFill.style.width = `${progress}%`
    }
    if (this.progressText) {
      this.progressText.textContent = `Pertanyaan ${this.questionCount + 1} dari ${this.maxQuestions}`
    }
    if (this.ingredientsCountEl) {
      this.ingredientsCountEl.textContent = `Bahan: ${this.ingredientsCount}/${this.minIngredients}`

      // Update color based on ingredients count
      if (this.ingredientsCount >= this.minIngredients) {
        this.ingredientsCountEl.style.background = "#27ae60"
        this.ingredientsCountEl.style.color = "white"
      } else {
        this.ingredientsCountEl.style.background = "#f39c12"
        this.ingredientsCountEl.style.color = "white"
      }
    }
  }

  updateQuestionCategory() {
    const question = this.currentQuestion.toLowerCase()
    let category = "Umum"
    let categoryColor = "#2c3e50"

    if (question.includes("telur")) {
      category = "Telur"
      categoryColor = "#f39c12"
    } else if (question.includes("daging") || question.includes("ayam") || question.includes("sapi")) {
      category = "Daging"
      categoryColor = "#e74c3c"
    } else if (question.includes("ikan")) {
      category = "Ikan"
      categoryColor = "#3498db"
    } else if (question.includes("nasi") || question.includes("beras")) {
      category = "Nasi/Beras"
      categoryColor = "#f1c40f"
    } else if (question.includes("mie")) {
      category = "Mie"
      categoryColor = "#e67e22"
    } else if (
      question.includes("sayur") ||
      question.includes("wortel") ||
      question.includes("kentang") ||
      question.includes("buncis")
    ) {
      category = "Sayuran"
      categoryColor = "#27ae60"
    } else if (question.includes("tahu") || question.includes("tempe")) {
      category = "Tahu/Tempe"
      categoryColor = "#95a5a6"
    } else if (question.includes("bawang")) {
      category = "Bawang"
      categoryColor = "#8e44ad"
    } else if (question.includes("cabai")) {
      category = "Cabai"
      categoryColor = "#c0392b"
    } else if (question.includes("tomat")) {
      category = "Tomat"
      categoryColor = "#e74c3c"
    } else if (question.includes("kecap")) {
      category = "Kecap"
      categoryColor = "#34495e"
    } else if (
      question.includes("bumbu") ||
      question.includes("garam") ||
      question.includes("minyak") ||
      question.includes("jahe") ||
      question.includes("santan") ||
      question.includes("tepung") ||
      question.includes("gula") ||
      question.includes("terasi")
    ) {
      category = "Bumbu & Rempah"
      categoryColor = "#d35400"
    } else if (question.includes("air")) {
      category = "Air"
      categoryColor = "#3498db"
    } else if (question.includes("teh") || question.includes("minuman")) {
      category = "Minuman"
      categoryColor = "#16a085"
    }

    if (this.questionCategory) {
      const categoryBadge = this.questionCategory.querySelector(".category-badge")
      if (categoryBadge) {
        categoryBadge.textContent = `Kategori: ${category}`
        categoryBadge.style.background = categoryColor
      }
    }
  }

  updateIngredientsPreview() {
    if (!this.currentIngredients) return

    this.currentIngredients.innerHTML = ""

    if (this.confirmedIngredients.length > 0) {
      this.confirmedIngredients.forEach((ingredient) => {
        const chip = document.createElement("span")
        chip.className = "ingredient-chip"
        chip.textContent = this.translateIngredient(ingredient)
        this.currentIngredients.appendChild(chip)
      })
    } else {
      this.currentIngredients.innerHTML = '<span class="ingredient-chip">Belum ada bahan yang dikonfirmasi</span>'
    }
  }

  updateLoadingStats(questions, ingredients) {
    if (this.loadingQuestions) {
      this.loadingQuestions.textContent = questions
    }
    if (this.loadingIngredients) {
      this.loadingIngredients.textContent = ingredients
    }
  }

  async answerQuestion(answer) {
    // Tambahkan efek visual pada tombol yang dipilih
    const selectedBtn = answer === "yes" ? this.yesBtn : this.noBtn
    if (selectedBtn) {
      selectedBtn.style.transform = "scale(0.95)"

      setTimeout(() => {
        selectedBtn.style.transform = ""
        this.showScreen(this.loadingScreen)
        this.updateLoadingStats(this.questionCount + 1, this.ingredientsCount)
      }, 200)
    }

    try {
      const response = await fetch("/answer", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: this.sessionId,
          answer: answer,
        }),
      })

      const data = await response.json()

      if (data.finished) {
        setTimeout(() => {
          this.showResults(data)
        }, 2000)
      } else if (data.question) {
        this.questionCount = data.question_count
        this.ingredientsCount = data.ingredients_count
        this.currentQuestion = data.question

        // Update confirmed ingredients
        if (data.available_ingredients) {
          this.confirmedIngredients = data.available_ingredients
        }

        // Delay untuk efek dramatis
        setTimeout(() => {
          this.showQuestion()
        }, 1500)
      } else {
        this.showError("Terjadi kesalahan dalam permainan")
      }
    } catch (error) {
      console.error("Error answering question:", error)
      this.showError("Terjadi kesalahan saat memproses jawaban")
    }
  }

  showResults(data) {
    if (data.recommendations && data.recommendations.length > 0) {
      this.displayRecommendations(data.recommendations)
      this.displayAvailableIngredients(data.available_ingredients)
      this.displaySummary(data)
      this.showScreen(this.resultsScreen)
    } else {
      this.showScreen(this.noResultsScreen)
    }
  }

  displaySummary(data) {
    if (this.totalQuestions) {
      this.totalQuestions.textContent = data.question_count
    }
    if (this.totalIngredients) {
      this.totalIngredients.textContent = data.total_ingredients
    }
    if (this.totalRecipes) {
      this.totalRecipes.textContent = data.recommendations.length
    }
  }

  displayRecommendations(recommendations) {
    if (!this.recommendationsList) return

    this.recommendationsList.innerHTML = ""

    recommendations.forEach((recipe, index) => {
      const recipeCard = document.createElement("div")
      recipeCard.className = "recipe-card"

      const matchPercentage = Math.round(recipe.match_percentage)

      // Tentukan class untuk match percentage
      let percentageClass = "low"
      let percentageIcon = "🔴"
      if (matchPercentage >= 80) {
        percentageClass = "high"
        percentageIcon = "🟢"
      } else if (matchPercentage >= 60) {
        percentageClass = "medium"
        percentageIcon = "🟡"
      }

      // Tentukan ranking badge
      let rankingBadge = ""
      if (index < 3) {
        const badges = ["🥇", "🥈", "🥉"]
        rankingBadge = `<span class="ranking-badge">${badges[index]}</span>`
      }

      let missingIngredientsHtml = ""
      if (recipe.missing_ingredients && recipe.missing_ingredients.length > 0) {
        const translatedIngredients = recipe.missing_ingredients.map((ing) => this.translateIngredient(ing))
        missingIngredientsHtml = `
                    <div class="missing-ingredients">
                        <strong>🛒 Bahan yang perlu ditambahkan:</strong>
                        <div class="missing-chips">
                            ${translatedIngredients.map((ing) => `<span class="missing-chip">${ing}</span>`).join("")}
                        </div>
                    </div>
                `
      }

      recipeCard.innerHTML = `
                <div class="recipe-header">
                    ${rankingBadge}
                    <h3>${index + 1}. ${recipe.name}</h3>
                    <span class="match-percentage ${percentageClass}">
                        ${percentageIcon} ${matchPercentage}% cocok
                    </span>
                </div>
                <p class="recipe-description">${recipe.description}</p>
                ${missingIngredientsHtml}
            `

      this.recommendationsList.appendChild(recipeCard)
    })
  }

  displayAvailableIngredients(ingredients) {
    if (!this.availableIngredients) return

    this.availableIngredients.innerHTML = ""

    if (ingredients && ingredients.length > 0) {
      // Kelompokkan bahan berdasarkan kategori
      const categorizedIngredients = this.categorizeIngredients(ingredients)

      Object.keys(categorizedIngredients).forEach((category) => {
        if (categorizedIngredients[category].length > 0) {
          const categoryDiv = document.createElement("div")
          categoryDiv.className = "ingredient-category"

          const categoryTitle = document.createElement("h5")
          categoryTitle.textContent = category
          categoryTitle.className = "category-title"
          categoryDiv.appendChild(categoryTitle)

          const categoryChips = document.createElement("div")
          categoryChips.className = "category-chips"

          categorizedIngredients[category].forEach((ingredient) => {
            const chip = document.createElement("span")
            chip.className = "ingredient-chip"
            chip.textContent = this.translateIngredient(ingredient)
            categoryChips.appendChild(chip)
          })

          categoryDiv.appendChild(categoryChips)
          this.availableIngredients.appendChild(categoryDiv)
        }
      })
    } else {
      this.availableIngredients.innerHTML = '<span class="ingredient-chip">Tidak ada bahan yang dikonfirmasi</span>'
    }
  }

  categorizeIngredients(ingredients) {
    const categories = {
      "🥚 Telur": [],
      "🥩 Daging": [],
      "🐟 Ikan": [],
      "🍚 Nasi/Beras": [],
      "🍜 Mie": [],
      "🥬 Sayuran": [],
      "🧄 Bawang": [],
      "🌶️ Cabai & Tomat": [],
      "🥄 Bumbu & Rempah": [],
      "🧀 Produk Olahan": [],
      "🥜 Kacang-kacangan": [],
      "🍵 Minuman": [],
      "🧊 Lainnya": [],
    }

    ingredients.forEach((ingredient) => {
      if (ingredient.includes("telur")) {
        categories["🥚 Telur"].push(ingredient)
      } else if (
        ingredient.includes("daging") ||
        ingredient.includes("ayam") ||
        ingredient.includes("sapi") ||
        ingredient.includes("bakso")
      ) {
        categories["🥩 Daging"].push(ingredient)
      } else if (ingredient.includes("ikan")) {
        categories["🐟 Ikan"].push(ingredient)
      } else if (ingredient.includes("nasi") || ingredient.includes("beras")) {
        categories["🍚 Nasi/Beras"].push(ingredient)
      } else if (ingredient.includes("mie")) {
        categories["🍜 Mie"].push(ingredient)
      } else if (ingredient.includes("sayur") || ingredient.includes("wortel") || ingredient.includes("kentang")) {
        categories["🥬 Sayuran"].push(ingredient)
      } else if (ingredient.includes("bawang")) {
        categories["🧄 Bawang"].push(ingredient)
      } else if (ingredient.includes("cabai") || ingredient.includes("tomat")) {
        categories["🌶️ Cabai & Tomat"].push(ingredient)
      } else if (
        ingredient.includes("garam") ||
        ingredient.includes("minyak") ||
        ingredient.includes("kecap") ||
        ingredient.includes("jahe") ||
        ingredient.includes("kunyit") ||
        ingredient.includes("santan") ||
        ingredient.includes("tepung") ||
        ingredient.includes("gula") ||
        ingredient.includes("terasi") ||
        ingredient.includes("lada") ||
        ingredient.includes("kluwek")
      ) {
        categories["🥄 Bumbu & Rempah"].push(ingredient)
      } else if (ingredient.includes("keju") || ingredient.includes("susu") || ingredient.includes("mentega")) {
        categories["🧀 Produk Olahan"].push(ingredient)
      } else if (ingredient.includes("kacang")) {
        categories["🥜 Kacang-kacangan"].push(ingredient)
      } else if (ingredient.includes("teh") || ingredient.includes("air")) {
        categories["🍵 Minuman"].push(ingredient)
      } else {
        categories["🧊 Lainnya"].push(ingredient)
      }
    })

    return categories
  }

  translateIngredient(ingredient) {
    const translations = {
      // Telur
      telur_ayam_banyak: "Telur Ayam (>3 butir)",
      telur_ayam_sedikit: "Telur Ayam (≤3 butir)",
      telur_bebek_banyak: "Telur Bebek (>3 butir)",
      telur_bebek_sedikit: "Telur Bebek (≤3 butir)",

      // Daging
      daging_ayam_banyak: "Daging Ayam (>500g)",
      daging_ayam_sedikit: "Daging Ayam (≤500g)",
      daging_sapi_tulang: "Daging Sapi Bertulang",
      daging_sapi_tanpa_tulang: "Daging Sapi Tanpa Tulang",
      bakso: "Bakso",

      // Ikan
      ikan_besar: "Ikan Besar",
      ikan_kecil: "Ikan Kecil-Sedang",
      ikan_teri: "Ikan Teri",

      // Nasi/Beras
      nasi_putih_banyak: "Nasi Putih (>3 porsi)",
      nasi_putih_sedikit: "Nasi Putih (≤3 porsi)",
      beras: "Beras",

      // Mie
      mie_instan_banyak: "Mie Instan (>3 bungkus)",
      mie_instan_sedikit: "Mie Instan (≤3 bungkus)",

      // Sayuran
      sayur_hijau_banyak: "Sayuran Hijau (>2 ikat)",
      sayur_hijau_sedikit: "Sayuran Hijau (≤2 ikat)",
      wortel: "Wortel",
      kentang: "Kentang",
      tomat: "Tomat",

      // Tahu Tempe
      tahu: "Tahu",
      tempe: "Tempe",

      // Bawang
      bawang_merah: "Bawang Merah",
      bawang_putih: "Bawang Putih",
      bawang_bombay: "Bawang Bombay",

      // Cabai
      cabai_banyak: "Cabai (>10 buah/suka pedas)",
      cabai_sedikit: "Cabai (≤10 buah/tidak suka pedas)",

      // Kecap
      kecap_manis: "Kecap Manis",
      kecap_asin: "Kecap Asin",

      // Bumbu & Rempah
      garam: "Garam",
      minyak_goreng_banyak: "Minyak Goreng (>500ml)",
      minyak_goreng_sedikit: "Minyak Goreng (≤500ml)",
      jahe: "Jahe",
      kunyit: "Kunyit",
      santan: "Santan",
      tepung_terigu: "Tepung Terigu",
      gula: "Gula Pasir",
      gula_merah: "Gula Merah/Jawa",
      terasi: "Terasi",
      lada_hitam: "Lada Hitam",
      kluwek: "Kluwek (Bumbu Rawon)",

      // Produk Olahan
      keju: "Keju",
      susu: "Susu",
      mentega: "Mentega/Margarin",

      // Kacang-kacangan
      kacang_tanah: "Kacang Tanah",

      // Minuman
      teh: "Teh",
      air_bersih: "Air Bersih",
    }

    return translations[ingredient] || ingredient
  }

  async restartGame() {
    if (this.sessionId) {
      try {
        await fetch("/restart", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            session_id: this.sessionId,
          }),
        })
      } catch (error) {
        console.error("Error restarting game:", error)
      }
    }

    this.sessionId = null
    this.currentQuestion = null
    this.questionCount = 0
    this.ingredientsCount = 0
    this.confirmedIngredients = []
    this.showScreen(this.welcomeScreen)
  }

  showError(message) {
    alert(message)
    this.showScreen(this.welcomeScreen)
  }
}

// Initialize the game when the page loads
document.addEventListener("DOMContentLoaded", () => {
  new EnhancedFoodAkinator()
})
