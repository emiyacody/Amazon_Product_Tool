document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const form = document.getElementById("analyze-form");
    const urlInput = document.getElementById("url-input");
    const rawTextInput = document.getElementById("raw-text-input");
    const urlGroup = document.getElementById("url-group");
    const rawTextGroup = document.getElementById("raw-text-group");
    const togglePasteBtn = document.getElementById("toggle-paste-btn");
    const submitBtn = document.getElementById("submit-btn");
    
    const loadingContainer = document.getElementById("loading-container");
    const statusText = document.getElementById("status-text");
    const stepScrape = document.getElementById("step-scrape");
    const stepAI = document.getElementById("step-ai");
    const stepFormat = document.getElementById("step-format");
    
    const placeholderCard = document.getElementById("placeholder-card");
    const resultContainer = document.getElementById("result-container");
    
    // Result displays
    const resName = document.getElementById("res-name");
    const resCategory = document.getElementById("res-category");
    const resPrice = document.getElementById("res-price");
    const resFeatures = document.getElementById("res-features");
    const resUsers = document.getElementById("res-users");
    const resScenarios = document.getElementById("res-scenarios");
    const resPainPoints = document.getElementById("res-pain-points");
    const resSellingPoints = document.getElementById("res-selling-points");
    
    const scriptContent = document.getElementById("script-content");
    const hookContent = document.getElementById("hook-content");
    const bodyContent = document.getElementById("body-content");
    const ctaContent = document.getElementById("cta-content");
    const charCounter = document.getElementById("char-counter");
    
    const copyBtn = document.getElementById("copy-btn");
    const speakBtn = document.getElementById("speak-btn");
    const voiceSelect = document.getElementById("voice-select");
    const downloadBtn = document.getElementById("download-btn");
    const styleSelect = document.getElementById("style-select");
    const regenerateBtn = document.getElementById("regenerate-btn");

    // State Variables
    let isPasteMode = false;
    let isSpeaking = false;
    let currentAudio = null;
    let audioUrl = null;
    let audioBlob = null;

    // Toggle Input Modes (URL vs Raw Paste)
    togglePasteBtn.addEventListener("click", () => {
        isPasteMode = !isPasteMode;
        if (isPasteMode) {
            urlGroup.classList.add("hidden");
            rawTextGroup.classList.remove("hidden");
            urlInput.value = "";
            togglePasteBtn.innerHTML = '<i class="fa-solid fa-link"></i> Switch to URL Extraction Mode';
        } else {
            urlGroup.classList.remove("hidden");
            rawTextGroup.classList.add("hidden");
            rawTextInput.value = "";
            togglePasteBtn.innerHTML = '<i class="fa-solid fa-code"></i> Switch to Raw Content / HTML Paste Mode (Fallback)';
        }
    });

    // Handle Form Submission
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        let url = urlInput.value.trim();
        if (url && !/^https?:\/\//i.test(url)) {
            url = "https://" + url;
        }
        const rawText = rawTextInput.value.trim();
        
        // Validation checks
        if (!isPasteMode && !url) {
            alert("Please enter an Amazon product URL!");
            return;
        }
        if (isPasteMode && !rawText) {
            alert("Please paste the product page HTML or raw text content!");
            return;
        }

        // Reset UI States
        submitBtn.disabled = true;
        resultContainer.classList.add("hidden");
        placeholderCard.classList.remove("hidden");
        loadingContainer.classList.remove("hidden");
        
        // Initialize loading steps
        resetLoadingSteps();
        updateLoadingStep(stepScrape, "active");
        
        statusText.textContent = isPasteMode ? "Parsing raw content..." : "Connecting to Amazon to extract product details...";

        // Set up fake timing offsets to show smooth visual status transitions
        let statusTimeout = setTimeout(() => {
            updateLoadingStep(stepScrape, "completed");
            updateLoadingStep(stepAI, "active");
            statusText.textContent = "Product details extracted! Gemini AI is conducting deep market analysis...";
        }, isPasteMode ? 1000 : 7000); // Scraping takes longer than local paste parsing

        let apiErrorOccurred = false;
        
        try {
            // Call Backend API
            const response = await fetch("/api/analyze", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    url: isPasteMode ? null : url,
                    raw_text: isPasteMode ? rawText : null,
                    style: styleSelect.value
                })
            });

            clearTimeout(statusTimeout);

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Request failed");
            }

            const data = await response.json();
            
            // Advance steps to formatting phase
            updateLoadingStep(stepScrape, "completed");
            updateLoadingStep(stepAI, "completed");
            updateLoadingStep(stepFormat, "active");
            statusText.textContent = "Analysis complete! Generating and checking voiceover script...";

            setTimeout(() => {
                updateLoadingStep(stepFormat, "completed");
                displayResults(data);
                
                // Hide loader and show results
                loadingContainer.classList.add("hidden");
                placeholderCard.classList.add("hidden");
                resultContainer.classList.remove("hidden");
                submitBtn.disabled = false;
            }, 1000);

        } catch (error) {
            clearTimeout(statusTimeout);
            apiErrorOccurred = true;
            alert(`Analysis failed: ${error.message}`);
            
            // Reset loaders
            loadingContainer.classList.add("hidden");
            submitBtn.disabled = false;
        }
    });

    // Handle Script Regeneration (Style change)
    regenerateBtn.addEventListener("click", async () => {
        let url = urlInput.value.trim();
        if (url && !/^https?:\/\//i.test(url)) {
            url = "https://" + url;
        }
        const rawText = rawTextInput.value.trim();

        if (!isPasteMode && !url) {
            alert("Please enter an Amazon product URL!");
            return;
        }
        if (isPasteMode && !rawText) {
            alert("Please paste the product page HTML or raw text content!");
            return;
        }

        // Disable UI controls
        regenerateBtn.disabled = true;
        regenerateBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generating...';
        submitBtn.disabled = true;
        
        // Reset audio state since script is changing
        resetAudioState();

        try {
            // Send request with selected style
            const response = await fetch("/api/analyze", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    url: isPasteMode ? null : url,
                    raw_text: isPasteMode ? rawText : null,
                    style: styleSelect.value
                })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Regeneration request failed");
            }

            const data = await response.json();
            
            // Re-display results
            displayResults(data);
            
        } catch (error) {
            console.error("Regeneration error:", error);
            alert(`Script regeneration failed: ${error.message}`);
        } finally {
            regenerateBtn.disabled = false;
            regenerateBtn.innerHTML = '<i class="fa-solid fa-rotate"></i> Regenerate Script';
            submitBtn.disabled = false;
        }
    });

    // Handle Copy to Clipboard
    copyBtn.addEventListener("click", () => {
        const text = scriptContent.textContent;
        if (!text) return;

        navigator.clipboard.writeText(text).then(() => {
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = '<i class="fa-solid fa-circle-check"></i> Copied to Clipboard';
            copyBtn.style.background = "#10b981";
            setTimeout(() => {
                copyBtn.innerHTML = originalText;
                copyBtn.style.background = "";
            }, 2000);
        }).catch(err => {
            console.error("Clipboard copy failed:", err);
            alert("Copy failed. Please manually select and copy the text!");
        });
    });

    // Stop audio player and clean up URL
    function stopAudio() {
        if (currentAudio) {
            currentAudio.pause();
            currentAudio = null;
        }
        isSpeaking = false;
        speakBtn.innerHTML = '<i class="fa-solid fa-play"></i> Preview Audio';
        speakBtn.classList.remove("primary");
    }

    // Reset audio state and URL
    function resetAudioState() {
        stopAudio();
        if (audioUrl) {
            URL.revokeObjectURL(audioUrl);
            audioUrl = null;
        }
        audioBlob = null;
        downloadBtn.disabled = true;
    }

    // Handle Text to Speech (Edge Neural TTS API)
    speakBtn.addEventListener("click", async () => {
        const text = scriptContent.textContent;
        if (!text) return;

        if (isSpeaking) {
            stopAudio();
            return;
        }

        // If audio is already loaded, replay it
        if (currentAudio && audioBlob) {
            playLoadedAudio();
            return;
        }

        // Otherwise, fetch TTS stream from backend
        try {
            speakBtn.disabled = true;
            speakBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Generating Audio...';
            
            const response = await fetch("/api/tts", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: text,
                    voice: voiceSelect.value
                })
            });

            if (!response.ok) {
                throw new Error("Speech synthesis failed");
            }

            audioBlob = await response.blob();
            
            if (audioUrl) {
                URL.revokeObjectURL(audioUrl);
            }
            audioUrl = URL.createObjectURL(audioBlob);
            
            // Enable download button
            downloadBtn.disabled = false;
            
            playLoadedAudio();
        } catch (error) {
            console.error("TTS error:", error);
            alert("Speech generation failed. Please try again!");
            stopAudio();
        } finally {
            speakBtn.disabled = false;
        }
    });

    function playLoadedAudio() {
        if (!audioUrl) return;
        
        currentAudio = new Audio(audioUrl);
        
        currentAudio.onplay = () => {
            isSpeaking = true;
            speakBtn.innerHTML = '<i class="fa-solid fa-stop"></i> Stop Audio';
            speakBtn.classList.add("primary");
        };

        currentAudio.onended = () => {
            stopAudio();
        };

        currentAudio.onerror = (e) => {
            console.error("Audio playback error:", e);
            alert("Audio playback error!");
            stopAudio();
        };

        currentAudio.play().catch(err => {
            console.error("Audio play failed:", err);
            stopAudio();
        });
    }

    // Handle Audio Downloading
    downloadBtn.addEventListener("click", () => {
        if (!audioBlob || !audioUrl) return;
        
        // Extract product name or first 15 characters for file name
        let rawName = resName.textContent || "Voiceover";
        let cleanName = rawName.replace(/[\\/:*?"<>|]/g, "").trim().substring(0, 15);
        let fileName = `${cleanName}_Voiceover.mp3`;

        const a = document.createElement("a");
        a.href = audioUrl;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    });

    // Reset audio state when voice changes
    voiceSelect.addEventListener("change", () => {
        resetAudioState();
    });

    // Reset audio state when style changes
    styleSelect.addEventListener("change", () => {
        resetAudioState();
    });

    // Helper functions for loading steps UI updates
    function resetLoadingSteps() {
        [stepScrape, stepAI, stepFormat].forEach(step => {
            step.className = "step";
            step.querySelector("i").className = "fa-solid fa-circle-notch fa-spin";
        });
    }

    function updateLoadingStep(stepElem, state) {
        if (state === "active") {
            stepElem.className = "step active";
            stepElem.querySelector("i").className = "fa-solid fa-spinner fa-spin";
        } else if (state === "completed") {
            stepElem.className = "step completed";
            stepElem.querySelector("i").className = "fa-solid fa-circle-check";
        }
    }

    // Populate Results into UI
    function displayResults(data) {
        // Stop and reset audio state
        resetAudioState();

        // 1. Basic Metadata
        resName.textContent = data.product_name || "N/A";
        resCategory.textContent = data.category || "N/A";
        resPrice.textContent = data.price || "N/A";
        
        // Features list
        resFeatures.innerHTML = "";
        if (data.core_features && data.core_features.length > 0) {
            data.core_features.forEach(feat => {
                const li = document.createElement("li");
                li.textContent = feat;
                resFeatures.appendChild(li);
            });
        } else {
            resFeatures.innerHTML = "<li>No specific features extracted</li>";
        }

        // 2. Audience & Scenario Tags
        resUsers.innerHTML = "";
        if (data.target_users && data.target_users.length > 0) {
            data.target_users.forEach(user => {
                const span = document.createElement("span");
                span.className = "tag";
                span.textContent = user;
                resUsers.appendChild(span);
            });
        } else {
            resUsers.innerHTML = "<span class='tag'>General Audience</span>";
        }

        resScenarios.innerHTML = "";
        if (data.usage_scenarios && data.usage_scenarios.length > 0) {
            data.usage_scenarios.forEach(scene => {
                const span = document.createElement("span");
                span.className = "tag";
                span.textContent = scene;
                resScenarios.appendChild(span);
            });
        } else {
            resScenarios.innerHTML = "<span class='tag'>Multi-Scenario</span>";
        }

        // 3. Pain Points and Selling Points
        populateList(resPainPoints, data.user_pain_points);
        populateList(resSellingPoints, data.core_selling_points);

        // 4. Video Script Details
        scriptContent.textContent = data.full_script || "";
        hookContent.textContent = data.video_hook || "";
        bodyContent.textContent = data.video_body || "";
        ctaContent.textContent = data.video_cta || "";
        
        // Word counter for English text (count words separated by whitespace)
        const fullScriptText = (data.full_script || "").trim();
        const wordCount = fullScriptText ? fullScriptText.split(/\s+/).length : 0;
        charCounter.textContent = `${wordCount} / 150 words`;
        if (wordCount > 150) {
            charCounter.style.color = "#ef4444";
        } else {
            charCounter.style.color = "";
        }
    }

    function populateList(ulElem, itemsList) {
        ulElem.innerHTML = "";
        if (itemsList && itemsList.length > 0) {
            itemsList.forEach(item => {
                const li = document.createElement("li");
                li.textContent = item;
                ulElem.appendChild(li);
            });
        } else {
            ulElem.innerHTML = "<li>No details available</li>";
        }
    }
});
