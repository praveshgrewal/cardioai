document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');

    const placeholderState = document.getElementById('placeholderState');
    const resultState = document.getElementById('resultState');

    const gaugeFill = document.getElementById('gaugeFill');
    const riskPercentageText = document.getElementById('riskPercentage');
    const riskLevelBadge = document.getElementById('riskLevelBadge');
    const riskSummaryText = document.getElementById('riskSummaryText');
    const recommendationsList = document.getElementById('recommendationsList');

    // Circumference of SVG gauge semi-circle (radius = 80, Arc angle = ~180deg)
    const MAX_DASH_OFFSET = 251.2;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Show Loading State
        submitBtn.disabled = true;
        btnText.textContent = "Processing Patient Data...";
        btnLoader.classList.remove('hidden');

        // Extract Form Data
        const formData = {
            age: parseInt(document.getElementById('age').value),
            sex: document.getElementById('sex').value,
            bmi: parseFloat(document.getElementById('bmi').value),
            resting_heart_rate: parseInt(document.getElementById('resting_heart_rate').value),
            resting_bp_systolic: parseInt(document.getElementById('resting_bp_systolic').value),
            resting_bp_diastolic: parseInt(document.getElementById('resting_bp_diastolic').value),
            max_heart_rate_achieved: parseInt(document.getElementById('max_heart_rate_achieved').value),
            st_depression: parseFloat(document.getElementById('st_depression').value),
            chest_pain_type: document.getElementById('chest_pain_type').value,
            exercise_induced_angina: document.getElementById('exercise_induced_angina').checked,
            cholesterol_total: parseInt(document.getElementById('cholesterol_total').value),
            hdl: parseInt(document.getElementById('hdl').value),
            ldl: parseInt(document.getElementById('ldl').value),
            triglycerides: parseInt(document.getElementById('triglycerides').value),
            fasting_blood_sugar: parseInt(document.getElementById('fasting_blood_sugar').value),
            hba1c: parseFloat(document.getElementById('hba1c').value),
            smoker_status: document.getElementById('smoker_status').value,
            exercise_minutes_per_week: parseInt(document.getElementById('exercise_minutes_per_week').value),
            stress_score: parseFloat(document.getElementById('stress_score').value),
            daily_steps: parseInt(document.getElementById('daily_steps').value),
            alcohol_units_per_week: parseFloat(document.getElementById('alcohol_units_per_week').value),
            sleep_hours: parseFloat(document.getElementById('sleep_hours').value),
            diet_quality_score: parseFloat(document.getElementById('diet_quality_score').value),
            family_history: document.getElementById('family_history').checked,
            wearable_owner: document.getElementById('wearable_owner').checked
        };

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (!result.success) {
                alert("Error in prediction: " + (result.error || "Unknown error"));
                return;
            }

            // Hide placeholder, display results
            placeholderState.classList.remove('active');
            placeholderState.classList.add('hidden');

            resultState.classList.remove('hidden');
            resultState.classList.add('active');

            // Update Percentage & Gauge Animation
            const probability = result.risk_percentage;
            riskPercentageText.textContent = `${probability.toFixed(1)}%`;
            riskPercentageText.style.color = result.risk_color;

            // Calculate SVG offset: 0% risk -> 251.2 offset (empty), 100% risk -> 0 offset (full)
            const targetOffset = MAX_DASH_OFFSET - (MAX_DASH_OFFSET * (probability / 100));
            gaugeFill.style.strokeDashoffset = targetOffset;
            gaugeFill.style.stroke = result.risk_color;

            // Update Risk Badge & Summary
            riskLevelBadge.textContent = result.risk_level;
            riskLevelBadge.className = `badge ${result.badge_class}`;

            if (result.prediction === 1) {
                riskSummaryText.textContent = `High likelihood of cardiovascular risk (${probability.toFixed(1)}%). Clinical consultation and preventative monitoring advised.`;
            } else {
                riskSummaryText.textContent = `Low likelihood of cardiovascular risk (${probability.toFixed(1)}%). Patient indicators remain within manageable baseline parameters.`;
            }

            // Render Clinical Recommendations
            recommendationsList.innerHTML = '';
            result.recommendations.forEach(rec => {
                const item = document.createElement('div');
                item.className = 'rec-item';
                item.innerHTML = `
                    <div class="rec-icon">${rec.icon}</div>
                    <div class="rec-content">
                        <h5>${rec.title}</h5>
                        <p>${rec.desc}</p>
                    </div>
                `;
                recommendationsList.appendChild(item);
            });

        } catch (error) {
            console.error("Prediction API Error:", error);
            alert("Failed to connect to predictive model backend.");
        } finally {
            // Restore Submit Button
            submitBtn.disabled = false;
            btnText.textContent = "Analyze Heart Disease Risk";
            btnLoader.classList.add('hidden');
        }
    });
});
