import { LightningElement, api, track } from 'lwc';

const RADIX = 10, ZERO = 0;

export default class KpiBar extends LightningElement {
    @api people = [];
    @api targetOrgNumber = ZERO;
    @track editingTarget = false;

    get inSeatCount() { return this.people.filter(person => person.Status__c === 'In-Seat').length; }
    get backfillCount() { return this.people.filter(person => person.Status__c === 'Backfill').length; }
    get netNewCount() { return this.people.filter(person => person.Status__c === 'Net New').length; }
    get totalCount() { return this.people.length; }
    get managersCount() { return this.people.filter(person => person.Role__c === 'People Manager').length; }
    get icCount() { return this.people.filter(person => person.Role__c === 'Individual Contributor').length; }
    get eaCount() { return this.people.filter(person => person.Role__c === 'Executive Assistant').length; }
    get internCount() { return this.people.filter(person => person.Role__c === 'FuturForce Intern').length; }
    get otherCount() { return this.people.filter(person => person.Role__c === 'Other').length; }
    get solutionsCount() { return this.people.filter(person => person.Type__c === 'Solutions').length; }
    get builderCount() { return this.people.filter(person => person.Type__c === 'Builder').length; }

    get gap() { return (this.targetOrgNumber || ZERO) - this.totalCount; }
    get gapDisplay() {
        const gapValue = this.gap;
        if (gapValue > ZERO) { return `+${gapValue}`; }
        return `${gapValue}`;
    }
    get gapPositive() { return this.gap >= ZERO; }

    startEditTarget() {
        this.editingTarget = true;
        Promise.resolve().then(() => {
            const input = this.template.querySelector('[data-id="target-input"]');
            if (input) { input.focus(); }
        });
    }

    handleTargetBlur(event) {
        this.commitTarget(event.target.value);
    }

    handleTargetKeydown(event) {
        if (event.key === 'Enter') { this.commitTarget(event.target.value); }
        if (event.key === 'Escape') { this.editingTarget = false; }
    }

    commitTarget(value) {
        const num = parseInt(value, RADIX);
        if (!isNaN(num) && num >= ZERO) {
            this.dispatchEvent(new CustomEvent('targetchange', { detail: num }));
        }
        this.editingTarget = false;
    }
}
